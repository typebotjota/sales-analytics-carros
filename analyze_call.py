# Sales Analytics Pro — Prompt de Analise Claude
# Contexto: Vendas Automotivas (Concessionarias e Revendedoras)
# Modelo: claude-sonnet-4-6
# Uso: Enviar transcricao da call como input

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

# ==================== SCRIPT DE ANALISE ====================
# analyze_call.py adaptado para Sales Analytics Pro

"""
Uso:
  python analyze_call.py transcricao.txt --closer "Carlos Silva" --date "2026-03-01"

Pipeline completo:
  1. audio.mp4 -> Whisper -> transcricao.txt
  2. transcricao.txt -> Claude API -> analise.json
  3. analise.json -> append calls_history.json -> dashboard atualiza
"""

import json
import sys
import os
from datetime import datetime

# Configuracao
CLAUDE_MODEL = "claude-sonnet-4-6"
CALLS_HISTORY_FILE = "calls_history.json"

def analyze_call(transcription_path, closer_name, call_date):
    """
    Envia transcricao para Claude API e retorna analise estruturada.
    """
    import anthropic
    
    client = anthropic.Anthropic()
    
    with open(transcription_path, 'r', encoding='utf-8') as f:
        transcription = f.read()
    
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analise esta call de venda automotiva.\n\nVendedor: {closer_name}\nData: {call_date}\n\nTRANSCRICAO:\n{transcription}"
            }
        ]
    )
    
    response_text = message.content[0].text
    
    # Limpar markdown se houver
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]
    
    analysis = json.loads(response_text.strip())
    
    # Garantir campos obrigatorios
    analysis['id'] = f"call-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    analysis['closer'] = closer_name
    analysis['date'] = call_date
    
    return analysis

def append_to_history(analysis):
    """
    Adiciona analise ao calls_history.json
    """
    history = []
    if os.path.exists(CALLS_HISTORY_FILE):
        with open(CALLS_HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    history.append(analysis)
    
    with open(CALLS_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"Call adicionada: {analysis['name']} — Score {analysis['score']} ({analysis['classification']})")
    return history

def transcribe_audio(audio_path):
    """
    Transcreve audio usando Whisper.
    """
    import whisper
    
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="pt")
    
    txt_path = audio_path.rsplit('.', 1)[0] + '.txt'
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    
    print(f"Transcricao salva em: {txt_path}")
    return txt_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Sales Analytics Pro - Analisador de Calls')
    parser.add_argument('input', help='Caminho do arquivo de audio ou transcricao (.txt)')
    parser.add_argument('--closer', required=True, help='Nome do vendedor')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='Data da call (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # Se for audio, transcrever primeiro
    if not args.input.endswith('.txt'):
        print(f"Transcrevendo {args.input}...")
        txt_path = transcribe_audio(args.input)
    else:
        txt_path = args.input
    
    # Analisar com Claude
    print(f"Analisando com Claude ({CLAUDE_MODEL})...")
    analysis = analyze_call(txt_path, args.closer, args.date)
    
    # Salvar no historico
    append_to_history(analysis)
    
    print(f"\nResultado:")
    print(f"  Cliente: {analysis['name']}")
    print(f"  Score: {analysis['score']} ({analysis['classification']})")
    print(f"  Veiculo: {analysis.get('veiculo_interesse', 'N/A')}")
    print(f"  Test Drive: {'Sim' if analysis.get('test_drive') else 'Nao'}")
    print(f"  Prob. Fechamento: {analysis.get('closing_probability', 0)}%")
