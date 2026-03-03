"""
parse_whatsapp.py — Parser para exports de WhatsApp (formato brasileiro)

Formatos suportados:
  [DD/MM/AAAA HH:MM] Nome: mensagem
  [DD/MM/AAAA HH:MM:SS] Nome: mensagem
  DD/MM/AAAA HH:MM - Nome: mensagem   (sem colchetes)

Uso:
  from parse_whatsapp import parse_whatsapp
  resultado = parse_whatsapp("conversa.txt")
  # resultado['vendedor'], resultado['cliente'], resultado['metricas'], resultado['conversa_texto']
"""

import re
from datetime import datetime
from collections import defaultdict

# Suporta [DD/MM/AAAA HH:MM], [DD/MM/AAAA HH:MM:SS] e DD/MM/AAAA HH:MM - Nome:
_MSG_PATTERN = re.compile(
    r'(?:\[(\d{2}/\d{2}/\d{4})[,\s]+(\d{2}:\d{2}(?::\d{2})?)\]'
    r'|(\d{2}/\d{2}/\d{4})[,\s]+(\d{2}:\d{2}(?::\d{2})?))'
    r'\s*[-–]?\s*([^:\n]+?):\s*(.*?)(?=(?:\[?\d{2}/\d{2}/\d{4})|\Z)',
    re.DOTALL
)

_SYSTEM_KEYWORDS = (
    'mensagens e chamadas são criptografadas',
    'messages and calls are end-to-end encrypted',
    'criou o grupo', 'adicionou', 'saiu do grupo',
    'foi adicionado', 'mudou o nome do grupo',
    'mudou o ícone', 'segurança dos seus dados',
    'imagem de fundo', 'você bloqueou',
)

_MEDIA_KEYWORDS = (
    'imagem ocultada', 'vídeo ocultado', 'video ocultado',
    'documento ocultado', '<mídia oculta>', '<media omitted>',
    'imagem omitida', 'gif ocultado',
)

_AUDIO_KEYWORDS = (
    'áudio ocultado', 'audio ocultado',
    '<áudio omitido>', 'audio omitido',
)


def parse_whatsapp(filepath):
    """
    Lê export de WhatsApp e retorna conversa + métricas.

    Returns:
        dict:
          - 'messages': list[dict{timestamp, sender, text}]
          - 'conversa_texto': str formatada para Claude
          - 'vendedor': str
          - 'cliente': str
          - 'duration': str "HH:MM" (do início ao fim da conversa)
          - 'metricas': dict com todas as métricas objetivas
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    messages = _parse_messages(raw)

    if not messages:
        raise ValueError(
            "Nenhuma mensagem encontrada. Verifique se o arquivo está no "
            "formato de export do WhatsApp: [DD/MM/AAAA HH:MM] Nome: mensagem"
        )

    vendedor, cliente = _identify_roles(messages)
    metricas = _calculate_metrics(messages, vendedor)
    conversa_texto = _format_conversation(messages, vendedor, cliente)
    duration = _calc_duration(messages)

    return {
        'messages': messages,
        'conversa_texto': conversa_texto,
        'vendedor': vendedor,
        'cliente': cliente,
        'duration': duration,
        'metricas': metricas,
    }


# ─── Parsing ──────────────────────────────────────────────────────────────────

def _parse_messages(raw):
    messages = []
    for m in _MSG_PATTERN.finditer(raw):
        date1, time1, date2, time2, sender, text = m.groups()
        date_str = date1 or date2
        time_str = (time1 or time2)[:5]  # sempre HH:MM
        sender = sender.strip()
        text = text.strip()

        if _is_system(sender, text):
            continue

        try:
            ts = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        except ValueError:
            continue

        messages.append({'timestamp': ts, 'sender': sender, 'text': text})

    return messages


def _is_system(sender, text):
    combined = (sender + ' ' + text).lower()
    return any(kw in combined for kw in _SYSTEM_KEYWORDS)


# ─── Identificação de papéis ──────────────────────────────────────────────────

def _identify_roles(messages):
    """
    Vendedor = participante com maior score.
    Score = (msgs longas > 50 chars) * 2 + total de msgs.
    Lógica: vendedores tendem a enviar mensagens mais elaboradas.
    """
    stats = defaultdict(lambda: {'total': 0, 'long': 0})
    for msg in messages:
        s = msg['sender']
        stats[s]['total'] += 1
        if len(msg['text']) > 50:
            stats[s]['long'] += 1

    senders = list(stats.keys())
    if len(senders) < 2:
        return senders[0], senders[0]

    scores = {s: v['long'] * 2 + v['total'] for s, v in stats.items()}
    ranked = sorted(scores, key=scores.get, reverse=True)
    return ranked[0], ranked[1]


# ─── Métricas ─────────────────────────────────────────────────────────────────

def _calculate_metrics(messages, vendedor):
    msg_v = [m for m in messages if m['sender'] == vendedor]
    msg_c = [m for m in messages if m['sender'] != vendedor]

    tempo_primeira_resposta = _first_response_time(messages, vendedor)
    tempo_medio_resposta = _avg_response_time(messages, vendedor)

    media_enviada = sum(
        1 for m in messages
        if any(kw in m['text'].lower() for kw in _MEDIA_KEYWORDS)
    )
    audios_enviados = sum(
        1 for m in messages
        if any(kw in m['text'].lower() for kw in _AUDIO_KEYWORDS)
    )

    follow_up_realizado = _detect_follow_up(messages, vendedor)
    horario_fora_expediente = any(
        m['timestamp'].hour < 8 or m['timestamp'].hour >= 19
        for m in messages
    )
    link_enviado = any(re.search(r'https?://', m['text']) for m in messages)

    return {
        'tempo_primeira_resposta': tempo_primeira_resposta,
        'tempo_medio_resposta': tempo_medio_resposta,
        'total_mensagens_vendedor': len(msg_v),
        'total_mensagens_cliente': len(msg_c),
        'media_enviada': media_enviada,
        'audios_enviados': audios_enviados,
        'follow_up_realizado': follow_up_realizado,
        'horario_fora_expediente': horario_fora_expediente,
        'link_enviado': link_enviado,
    }


def _first_response_time(messages, vendedor):
    """Tempo (min) desde o 1º msg do cliente até a 1ª resposta do vendedor."""
    for i, msg in enumerate(messages):
        if msg['sender'] != vendedor:
            for j in range(i + 1, len(messages)):
                if messages[j]['sender'] == vendedor:
                    diff = (messages[j]['timestamp'] - msg['timestamp']).total_seconds() / 60
                    return round(max(diff, 0), 1)
            break
    return None


def _avg_response_time(messages, vendedor):
    """Tempo médio (min) entre cada msg do cliente e a próxima resposta do vendedor."""
    times = []
    for i, msg in enumerate(messages):
        if msg['sender'] != vendedor:
            for j in range(i + 1, len(messages)):
                if messages[j]['sender'] == vendedor:
                    diff = (messages[j]['timestamp'] - msg['timestamp']).total_seconds() / 60
                    if diff >= 0:
                        times.append(diff)
                    break
    return round(sum(times) / len(times), 1) if times else None


def _detect_follow_up(messages, vendedor):
    """True se o vendedor enviou msg após 24h+ de silêncio do cliente."""
    for i in range(1, len(messages)):
        if messages[i]['sender'] == vendedor:
            last_cliente_ts = None
            for j in range(i - 1, -1, -1):
                if messages[j]['sender'] != vendedor:
                    last_cliente_ts = messages[j]['timestamp']
                    break
            if last_cliente_ts:
                silence_h = (messages[i]['timestamp'] - last_cliente_ts).total_seconds() / 3600
                if silence_h >= 24:
                    return True
    return False


def _calc_duration(messages):
    if len(messages) < 2:
        return "00:00"
    total_mins = int((messages[-1]['timestamp'] - messages[0]['timestamp']).total_seconds() / 60)
    h, m = divmod(total_mins, 60)
    return f"{h:02d}:{m:02d}"


# ─── Formatação para Claude ───────────────────────────────────────────────────

def _format_conversation(messages, vendedor, cliente):
    lines = []
    for msg in messages:
        role = "VENDEDOR" if msg['sender'] == vendedor else "CLIENTE"
        ts = msg['timestamp'].strftime("%d/%m %H:%M")
        lines.append(f"[{ts}] {role} ({msg['sender']}): {msg['text']}")
    return "\n".join(lines)


# ─── CLI (uso direto) ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Uso: python parse_whatsapp.py conversa.txt")
        sys.exit(1)

    resultado = parse_whatsapp(sys.argv[1])
    print(f"Vendedor identificado : {resultado['vendedor']}")
    print(f"Cliente identificado  : {resultado['cliente']}")
    print(f"Total de mensagens    : {len(resultado['messages'])}")
    print(f"Duração da conversa   : {resultado['duration']}")
    print("\nMétricas:")
    print(json.dumps(resultado['metricas'], ensure_ascii=False, indent=2))
