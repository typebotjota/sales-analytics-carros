# Sales Analytics Pro — Analisador Multi-Canal
# Contexto: Vendas Automotivas (Concessionárias e Revendedoras)
# Modelo: claude-sonnet-4-6
# Canais suportados: ligacao | whatsapp | presencial

# ==================== PROMPTS ====================

SYSTEM_PROMPT = """
Voce e um analista de vendas automotivas especializado em metodologias NEPQ (Neuro-Emotional Persuasion Questions) e Hormozi (stack de valor, custo da inacao, reversao de risco).

Sua funcao: analisar transcricoes de calls de venda de veiculos e retornar um JSON estruturado com metricas especificas do nicho automotivo.

DIMENSOES DE PERFORMANCE (score 1-10 para cada):

1. ABORDAGEM & RAPPORT (abordagem)
   - O vendedor criou conexao genuina?
   - Usou o nome do cliente?
   - Identificou perfil antes de falar de carro?
   - Score 9-10: Rapport excepcional, conexao emocional
   - Score 7-8: Boa abordagem, cordial
   - Score 5-6: Mecanica, sem conexao
   - Score 1-4: Fria, apressada, ja falou de preco

2. QUALIFICACAO (qualificacao)
   - Descobriu: necessidade real, prazo, budget, decisor?
   - Perguntas NEPQ de situacao e problema?
   - Score 9-10: Mapeou completamente situacao do cliente
   - Score 7-8: Boa qualificacao, faltou 1-2 pontos
   - Score 5-6: Superficial
   - Score 1-4: Nao qualificou / foi direto ao produto

3. APRESENTACAO DO VEICULO (apresentacao)
   - Conectou features com necessidades descobertas?
   - Argumentou valor vs concorrencia?
   - Score 9-10: Apresentacao personalizada, conectada com dor
   - Score 7-8: Boa apresentacao, generica em partes
   - Score 5-6: Lista de features sem contexto
   - Score 1-4: Nao apresentou ou so falou preco

4. TEST DRIVE (test_drive)
   - Ofereceu test drive?
   - Conduziu de forma emocional?
   - Destacou beneficios durante o test drive?
   - Score 9-10: TD realizado com conducao emocional
   - Score 7-8: TD oferecido e realizado
   - Score 5-6: TD oferecido mas mal conduzido
   - Score 1-4: NAO ofereceu test drive (erro critico)

5. TRATAMENTO DE OBJECOES (objecoes)
   - Identificou objecao real vs cortina de fumaca?
   - Usou tecnicas NEPQ ou Hormozi para reverter?
   - Score 9-10: Reverteu todas com maestria
   - Score 7-8: Reverteu maioria
   - Score 5-6: Tentou mas sem tecnica
   - Score 1-4: Aceitou objecoes sem lutar

6. FECHAMENTO (fechamento)
   - Pediu comprometimento com clareza?
   - Usou escassez ou urgencia real?
   - Score 9-10: Fechamento assertivo e natural
   - Score 7-8: Tentou fechar com boa tecnica
   - Score 5-6: Tentou sem assertividade
   - Score 1-4: Nao tentou fechar ou recuou

7. POS-VENDA (pos_venda)
   - Agendou proximo passo concreto?
   - Definiu follow-up?
   - Score 9-10: Proximo passo agendado com data/hora
   - Score 7-8: Follow-up definido
   - Score 5-6: Vago ("te ligo depois")
   - Score 1-4: Sem proximo passo

METRICAS AUTOMOTIVAS (extrair da conversa):
- test_drive: boolean (ofereceu E realizou?)
- proposta_enviada: boolean (enviou proposta formal?)
- financiamento_qualificado: boolean (discutiu e qualificou financiamento?)
- entrada_disponivel: string (valor identificado ou "Nao identificada")
- veiculo_interesse: string (modelo e ano)
- urgencia_compra: string (nivel e prazo)

OBJECOES TIPICAS DO NICHO (identificar na conversa):
- "Vou pesquisar mais" / "Vou ver em outras lojas"
- "Esta caro" / "Vi mais barato em outro lugar"
- "Preciso falar com minha esposa/socio"
- "Nao sei se o financiamento vai aprovar"
- "Vou esperar mais um pouco"
- "Quero primeiro vender meu carro atual"
- "Nao gostei da cor / do modelo"
- "Vou pensar e te ligo"

ANALISE NEPQ (score 1-10 para cada fase):
- situacao: Perguntas de contexto do cliente
- problema: Identificacao da dor real
- implicacao: Custo emocional/financeiro do problema
- fechamento: Solicitacao de compromisso

ANALISE HORMOZI (score 1-10 para cada):
- stack_valor: Construiu valor antes do preco?
- custo_inacao: Calculou quanto custa NAO comprar?
- reversao_risco: Ofereceu garantias para remover medo?

RETORNAR EXCLUSIVAMENTE UM JSON VALIDO com esta estrutura:
{
  "name": "Nome do Cliente",
  "closer": "Nome do Vendedor",
  "date": "YYYY-MM-DD",
  "duration": "MM:SS",
  "score": 0.0,
  "classification": "Boa|Regular|Fraca",
  "closing_probability": 0,
  "veiculo_interesse": "",
  "test_drive": false,
  "proposta_enviada": false,
  "financiamento_qualificado": false,
  "entrada_disponivel": "",
  "urgencia_compra": "",
  "performance": {
    "abordagem": 0.0,
    "qualificacao": 0.0,
    "apresentacao": 0.0,
    "test_drive": 0.0,
    "objecoes": 0.0,
    "fechamento": 0.0,
    "pos_venda": 0.0
  },
  "objections": [
    { "type": "", "handled": false, "quality": "Excelente|Boa|Regular|Fraca", "moment": "MM:SS" }
  ],
  "top_improvements": ["", "", ""],
  "next_step": "",
  "critical_moments": [
    { "time": "MM:SS", "type": "positivo|negativo", "desc": "" }
  ],
  "nepq_analysis": {
    "situacao": 0,
    "problema": 0,
    "implicacao": 0,
    "fechamento": 0
  },
  "hormozi_analysis": {
    "stack_valor": 0,
    "custo_inacao": 0,
    "reversao_risco": 0
  },
  "resumo": ""
}

REGRAS:
- Score geral = media ponderada das 7 dimensoes
- classification: >= 7 "Boa", >= 5 "Regular", < 5 "Fraca"
- closing_probability: estimar com base na qualificacao e engajamento
- top_improvements: exatamente 3, especificas e acionaveis
- critical_moments: 2-4 momentos mais importantes (positivos e negativos)
- resumo: maximo 2 frases, direto ao ponto
- Ser HONESTO e DURO na avaliacao — o objetivo e melhorar o vendedor
- Se o vendedor NAO ofereceu test drive, score de test_drive maximo = 3
- Se o vendedor comecou falando de preco sem qualificar, score maximo de qualificacao = 5
"""

SYSTEM_PROMPT_WHATSAPP = """
Voce e um analista de vendas automotivas especializado em metodologias NEPQ e Hormozi, com expertise em analise de conversas digitais.

Sua funcao: analisar conversas de WhatsApp de vendas automotivas e retornar um JSON estruturado com metricas especificas.

CONTEXTO DO CANAL:
- Estamos analisando uma conversa de WhatsApp (nao uma ligacao de voz)
- Test drive aqui significa: o vendedor convidou E agendou o test drive via chat
- As objecoes terao timestamps no formato "DD/MM HH:MM"
- Metricas objetivas (tempos, contagens) sao fornecidas no input — use-as para embasar os scores

DIMENSOES DE PERFORMANCE (score 1-10):

1. ABORDAGEM & RAPPORT (abordagem)
   - Criou conexao genuina por texto? Tom adequado para o canal?
   - Personalizou mensagens ou usou copy/cola?
   - Score 9-10: Rapport excelente, mensagens personalizadas
   - Score 5-6: Mecanico, copia/cola evidente
   - Score 1-4: Frio, impessoal ou agressivo

2. QUALIFICACAO (qualificacao)
   - Descobriu necessidade real, prazo, budget, decisor via perguntas?
   - Score 9-10: Qualificacao completa via chat
   - Score 1-4: Foi direto para preco sem qualificar

3. APRESENTACAO DO VEICULO (apresentacao)
   - Enviou fotos, videos, fichas tecnicas?
   - Conectou features com necessidades descobertas?
   - Score 9-10: Apresentacao rica com midia personalizada
   - Score 1-4: Enviou apenas preco ou lista generica

4. TEST DRIVE (test_drive)
   - Convidou e agendou test drive via chat?
   - Score 9-10: Agendou com data/hora confirmada
   - Score 7-8: Convidou e cliente demonstrou interesse
   - Score 5-6: Mencionou mas sem comprometimento
   - Score 1-4: NAO convidou para test drive (erro critico)

5. TRATAMENTO DE OBJECOES (objecoes)
   - Identificou e reverteu objecoes via texto?
   - Score 9-10: Reverteu todas com maestria
   - Score 1-4: Aceitou objecoes sem questionar

6. FECHAMENTO (fechamento)
   - Pediu comprometimento concreto (visita, test drive, assinatura)?
   - Score 9-10: Fechamento assertivo com data/hora definidos
   - Score 1-4: Nao tentou fechar

7. POS-VENDA (pos_venda)
   - Definiu proximo passo claro? Fez follow-up?
   - Score 9-10: Proximo passo agendado com data/hora
   - Score 1-4: Sem proximo passo definido

METRICAS AUTOMOTIVAS (extrair da conversa):
- test_drive: boolean (convidou E cliente aceitou/agendou?)
- proposta_enviada: boolean (enviou simulacao ou proposta formal?)
- financiamento_qualificado: boolean (discutiu financiamento com dados reais?)
- entrada_disponivel: string
- veiculo_interesse: string
- urgencia_compra: string

IMPORTANTE SOBRE AS METRICAS FORNECIDAS:
- Se tempo_primeira_resposta > 60 min: penalize abordagem e pos_venda
- Se tempo_medio_resposta > 30 min: penalize qualificacao e fechamento
- Se follow_up_realizado = true: bonifique pos_venda (+0.5)
- Se media_enviada = 0 e audios_enviados = 0: penalize apresentacao
- Se horario_fora_expediente = true: mencione no resumo como ponto positivo

RETORNAR EXCLUSIVAMENTE UM JSON VALIDO com esta estrutura:
{
  "name": "Nome do Cliente",
  "closer": "Nome do Vendedor",
  "date": "YYYY-MM-DD",
  "duration": "HH:MM",
  "score": 0.0,
  "classification": "Boa|Regular|Fraca",
  "closing_probability": 0,
  "veiculo_interesse": "",
  "test_drive": false,
  "proposta_enviada": false,
  "financiamento_qualificado": false,
  "entrada_disponivel": "",
  "urgencia_compra": "",
  "performance": {
    "abordagem": 0.0,
    "qualificacao": 0.0,
    "apresentacao": 0.0,
    "test_drive": 0.0,
    "objecoes": 0.0,
    "fechamento": 0.0,
    "pos_venda": 0.0
  },
  "objections": [
    { "type": "", "handled": false, "quality": "Excelente|Boa|Regular|Fraca", "moment": "DD/MM HH:MM" }
  ],
  "top_improvements": ["", "", ""],
  "next_step": "",
  "critical_moments": [
    { "time": "DD/MM HH:MM", "type": "positivo|negativo", "desc": "" }
  ],
  "nepq_analysis": {
    "situacao": 0,
    "problema": 0,
    "implicacao": 0,
    "fechamento": 0
  },
  "hormozi_analysis": {
    "stack_valor": 0,
    "custo_inacao": 0,
    "reversao_risco": 0
  },
  "resumo": ""
}

REGRAS:
- Score geral = media ponderada das 7 dimensoes
- classification: >= 7 "Boa", >= 5 "Regular", < 5 "Fraca"
- top_improvements: exatamente 3, especificas para canal WhatsApp
- critical_moments: 2-4 momentos mais importantes
- resumo: maximo 2 frases
- Se o vendedor NAO convidou para test drive, score de test_drive maximo = 3
- Ser HONESTO e DURO — o objetivo e melhorar o vendedor
"""

SYSTEM_PROMPT_PRESENCIAL = """
Voce e um analista de vendas automotivas especializado em metodologias NEPQ e Hormozi.

Sua funcao: analisar formularios de atendimento presencial de vendas automotivas e retornar um JSON estruturado.

CONTEXTO DO CANAL:
- Estamos analisando um atendimento PRESENCIAL em showroom ou patio
- Os dados vem de um formulario preenchido pelo vendedor apos o atendimento
- Checkboxes marcados (true) = acao realizada
- Campos vazios ou ausentes = acao possivelmente nao realizada
- Combine dados objetivos com notas do vendedor para inferir a qualidade
- Um checkbox true sem nota qualitativa = score medio (5-6)

COMO INTERPRETAR:
- Se test_drive_realizado = true + nota positiva => score test_drive alto
- Se proposta_enviada = false => score fechamento penalizado
- Se financiamento_discutido = true mas sem dados (entrada, prazo) => qualificacao media
- Notas do vendedor em "observacoes" e "proximos_passos" sao gold

DIMENSOES DE PERFORMANCE (score 1-10):

1. ABORDAGEM & RAPPORT (abordagem)
   - Como foi a recepcao? Cliente se sentiu bem-vindo?
   - Infira pelo contexto e notas

2. QUALIFICACAO (qualificacao)
   - Mapeou necessidade, prazo, budget, decisor?
   - Campos preenchidos = qualificacao feita

3. APRESENTACAO (apresentacao)
   - Mostrou veiculo de forma personalizada?
   - Usou argumentos de valor ou so preco?

4. TEST DRIVE (test_drive)
   - Realizou test drive? Como foi conduzido?
   - Se nao realizado: score maximo = 3

5. TRATAMENTO DE OBJECOES (objecoes)
   - Identificou e reverteu objecoes?

6. FECHAMENTO (fechamento)
   - Pediu comprometimento? Tentou fechar na hora?
   - proposta_enviada = true eleva este score

7. POS-VENDA (pos_venda)
   - Definiu proximo passo concreto?
   - Campo proximos_passos preenchido = bom sinal

METRICAS AUTOMOTIVAS: extrair dos campos do formulario

CRITICAL MOMENTS: descreva momentos-chave inferidos dos dados. Use "N/A" para o campo "time".

RETORNAR EXCLUSIVAMENTE UM JSON VALIDO com esta estrutura:
{
  "name": "Nome do Cliente",
  "closer": "Nome do Vendedor",
  "date": "YYYY-MM-DD",
  "duration": "MM:SS",
  "score": 0.0,
  "classification": "Boa|Regular|Fraca",
  "closing_probability": 0,
  "veiculo_interesse": "",
  "test_drive": false,
  "proposta_enviada": false,
  "financiamento_qualificado": false,
  "entrada_disponivel": "",
  "urgencia_compra": "",
  "performance": {
    "abordagem": 0.0,
    "qualificacao": 0.0,
    "apresentacao": 0.0,
    "test_drive": 0.0,
    "objecoes": 0.0,
    "fechamento": 0.0,
    "pos_venda": 0.0
  },
  "objections": [
    { "type": "", "handled": false, "quality": "Excelente|Boa|Regular|Fraca", "moment": "N/A" }
  ],
  "top_improvements": ["", "", ""],
  "next_step": "",
  "critical_moments": [
    { "time": "N/A", "type": "positivo|negativo", "desc": "" }
  ],
  "nepq_analysis": {
    "situacao": 0,
    "problema": 0,
    "implicacao": 0,
    "fechamento": 0
  },
  "hormozi_analysis": {
    "stack_valor": 0,
    "custo_inacao": 0,
    "reversao_risco": 0
  },
  "resumo": ""
}

REGRAS:
- Score geral = media ponderada das 7 dimensoes
- classification: >= 7 "Boa", >= 5 "Regular", < 5 "Fraca"
- top_improvements: exatamente 3, especificas para atendimento presencial
- resumo: maximo 2 frases
- Ser HONESTO e DURO — o objetivo e melhorar o vendedor
"""

# ==================== SCRIPT DE ANALISE ====================

"""
Uso:
  # Ligacao (audio ou transcricao .txt):
  python analyze_call.py audio.mp4 --closer "Carlos Silva" --date "2026-03-01"
  python analyze_call.py transcricao.txt --closer "Carlos Silva" --canal ligacao

  # WhatsApp (export .txt):
  python analyze_call.py conversa.txt --closer "Carlos Silva" --canal whatsapp

  # Presencial (formulario .json):
  python analyze_call.py formulario.json --closer "Carlos Silva" --canal presencial

Pipeline completo:
  1. [ligacao]   audio.mp4 -> Whisper -> transcricao.txt -> Claude -> calls_history.json
  2. [whatsapp]  conversa.txt -> parse_whatsapp -> Claude -> calls_history.json
  3. [presencial] formulario.json -> Claude -> calls_history.json
"""

import json
import sys
import os
from datetime import datetime

CLAUDE_MODEL = "claude-sonnet-4-6"
CALLS_HISTORY_FILE = "calls_history.json"


# ─── Helpers compartilhados ───────────────────────────────────────────────────

def _clean_json(response_text):
    """Remove markdown code fences do response do Claude, se presentes."""
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]
    return response_text.strip()


def _call_claude(system_prompt, user_content):
    import anthropic
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    return message.content[0].text


# ─── Canal: LIGACAO ───────────────────────────────────────────────────────────

def transcribe_audio(audio_path):
    """Transcreve audio usando Whisper."""
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="pt")
    txt_path = audio_path.rsplit('.', 1)[0] + '.txt'
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    print(f"Transcricao salva em: {txt_path}")
    return txt_path


def analyze_call(transcription_path, closer_name, call_date):
    """Envia transcricao para Claude e retorna analise estruturada."""
    with open(transcription_path, 'r', encoding='utf-8') as f:
        transcription = f.read()

    user_content = (
        f"Analise esta call de venda automotiva.\n\n"
        f"Vendedor: {closer_name}\nData: {call_date}\n\n"
        f"TRANSCRICAO:\n{transcription}"
    )
    response_text = _call_claude(SYSTEM_PROMPT, user_content)
    analysis = json.loads(_clean_json(response_text))

    analysis['id'] = f"call-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    analysis['canal'] = 'ligacao'
    analysis['closer'] = closer_name
    analysis['date'] = call_date
    analysis['canal_data'] = None
    return analysis


# ─── Canal: WHATSAPP ──────────────────────────────────────────────────────────

def analyze_whatsapp(filepath, closer_name, call_date):
    """Parseia conversa WhatsApp e envia para Claude com prompt adaptado."""
    from parse_whatsapp import parse_whatsapp

    parsed = parse_whatsapp(filepath)
    metricas = parsed['metricas']

    metricas_txt = "\n".join(
        f"  {k}: {v}" for k, v in metricas.items()
    )

    user_content = (
        f"Analise esta conversa de vendas automotivas via WhatsApp.\n\n"
        f"Vendedor identificado: {parsed['vendedor']}\n"
        f"Cliente identificado: {parsed['cliente']}\n"
        f"Data de referencia: {call_date}\n"
        f"Duracao total da conversa: {parsed['duration']}\n\n"
        f"METRICAS OBJETIVAS (pre-calculadas):\n{metricas_txt}\n\n"
        f"CONVERSA:\n{parsed['conversa_texto']}"
    )

    response_text = _call_claude(SYSTEM_PROMPT_WHATSAPP, user_content)
    analysis = json.loads(_clean_json(response_text))

    # Sobrescreve campos que o parser calcula com precisao
    analysis['id'] = f"whatsapp-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    analysis['canal'] = 'whatsapp'
    analysis['closer'] = closer_name or parsed['vendedor']
    analysis['date'] = call_date
    analysis['duration'] = parsed['duration']
    analysis['canal_data'] = metricas
    return analysis


# ─── Canal: PRESENCIAL ────────────────────────────────────────────────────────

def analyze_presencial(filepath, closer_name, call_date):
    """Le formulario presencial (.json) e envia para Claude com prompt adaptado."""
    with open(filepath, 'r', encoding='utf-8') as f:
        formulario = json.load(f)

    # Injeta closer e date no formulario se nao presentes
    if closer_name and 'vendedor' not in formulario:
        formulario['vendedor'] = closer_name
    if call_date and 'data' not in formulario:
        formulario['data'] = call_date

    user_content = (
        f"Analise este formulario de atendimento presencial automotivo.\n\n"
        f"FORMULARIO JSON:\n{json.dumps(formulario, ensure_ascii=False, indent=2)}"
    )

    response_text = _call_claude(SYSTEM_PROMPT_PRESENCIAL, user_content)
    analysis = json.loads(_clean_json(response_text))

    analysis['id'] = f"presencial-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    analysis['canal'] = 'presencial'
    analysis['closer'] = closer_name or analysis.get('closer', '')
    analysis['date'] = call_date
    analysis['canal_data'] = formulario
    return analysis


# ─── Historico ────────────────────────────────────────────────────────────────

def append_to_history(analysis):
    """Adiciona analise ao calls_history.json."""
    history = []
    if os.path.exists(CALLS_HISTORY_FILE):
        with open(CALLS_HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)

    history.append(analysis)

    with open(CALLS_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    canal = analysis.get('canal', 'ligacao')
    print(f"[{canal.upper()}] Adicionado: {analysis['name']} — Score {analysis['score']} ({analysis['classification']})")
    return history


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Sales Analytics Pro - Analisador Multi-Canal')
    parser.add_argument('input', help='Arquivo de entrada: audio/transcricao (.txt) para ligacao, .txt para whatsapp, .json para presencial')
    parser.add_argument('--closer', required=True, help='Nome do vendedor')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='Data do atendimento (YYYY-MM-DD)')
    parser.add_argument(
        '--canal',
        choices=['ligacao', 'whatsapp', 'presencial'],
        default='ligacao',
        help='Canal do atendimento (default: ligacao)',
    )

    args = parser.parse_args()

    if args.canal == 'whatsapp':
        print(f"Processando conversa WhatsApp: {args.input}")
        print("Parseando mensagens...")
        analysis = analyze_whatsapp(args.input, args.closer, args.date)

    elif args.canal == 'presencial':
        print(f"Processando formulario presencial: {args.input}")
        print(f"Analisando com Claude ({CLAUDE_MODEL})...")
        analysis = analyze_presencial(args.input, args.closer, args.date)

    else:  # ligacao (default)
        if not args.input.endswith('.txt'):
            print(f"Transcrevendo {args.input} com Whisper...")
            txt_path = transcribe_audio(args.input)
        else:
            txt_path = args.input

        print(f"Analisando com Claude ({CLAUDE_MODEL})...")
        analysis = analyze_call(txt_path, args.closer, args.date)

    append_to_history(analysis)

    canal_label = analysis.get('canal', 'ligacao').upper()
    print(f"\nResultado [{canal_label}]:")
    print(f"  Cliente  : {analysis['name']}")
    print(f"  Score    : {analysis['score']} ({analysis['classification']})")
    print(f"  Veiculo  : {analysis.get('veiculo_interesse', 'N/A')}")
    print(f"  Test Drive: {'Sim' if analysis.get('test_drive') else 'Nao'}")
    print(f"  Prob. Fechamento: {analysis.get('closing_probability', 0)}%")

    if analysis.get('canal_data') and args.canal == 'whatsapp':
        cd = analysis['canal_data']
        print(f"\n  Metricas WhatsApp:")
        print(f"    Tempo 1a resposta : {cd.get('tempo_primeira_resposta')} min")
        print(f"    Tempo medio resp  : {cd.get('tempo_medio_resposta')} min")
        print(f"    Msgs vendedor     : {cd.get('total_mensagens_vendedor')}")
        print(f"    Msgs cliente      : {cd.get('total_mensagens_cliente')}")
        print(f"    Midias enviadas   : {cd.get('media_enviada')}")
        print(f"    Audios enviados   : {cd.get('audios_enviados')}")
        print(f"    Follow-up 24h+    : {'Sim' if cd.get('follow_up_realizado') else 'Nao'}")
        print(f"    Fora expediente   : {'Sim' if cd.get('horario_fora_expediente') else 'Nao'}")
        print(f"    Link enviado      : {'Sim' if cd.get('link_enviado') else 'Nao'}")
