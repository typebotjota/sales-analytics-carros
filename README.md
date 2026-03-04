# Sales Analytics Pro 🚗

Plataforma de análise de performance de vendas para concessionárias e lojas de carros. Analisa atendimentos de 3 canais — ligações, WhatsApp e visitas presenciais — usando IA (Claude + Whisper) para gerar scores, insights acionáveis e mentoria de vendas personalizada.

---

## ✨ Funcionalidades

| Feature | Descrição |
|---|---|
| **Dashboard Multi-Canal** | Filtros por canal, vendedor e classificação em tempo real |
| **Score de Performance** | Avalia 7 dimensões: Abordagem, Qualificação, Apresentação, Test Drive, Objeções, Fechamento, Pós-venda |
| **Metodologias NEPQ + Hormozi** | Análise automática das técnicas de venda aplicadas |
| **Mapa de Objeções** | Ranking com canal mais frequente e scripts anti-objeção |
| **DNA do Closer** | Perfil de performance individual por vendedor |
| **Formulário Presencial** | App mobile-first para registrar atendimentos na loja |
| **Relatório Consolidado** | Performance por canal + plano de ação da equipe |

---

## 🏗️ Estrutura do Projeto

```
sales-analytics-carros/
├── index.html            # Dashboard principal (GitHub Pages)
├── form_presencial.html  # Formulário mobile-first para atendimentos na loja
├── analyze_call.py       # CLI: analisa calls via Claude API
├── parse_whatsapp.py     # Parser de conversas exportadas do WhatsApp
├── calls_history.json    # Histórico de atendimentos analisados
├── config.json           # Configurações da empresa e canais
└── README.md
```

---

## 🚀 Instalação

### Pré-requisitos

```bash
python 3.9+
pip install anthropic
```

### Configurar API

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Clonar e abrir

```bash
git clone https://github.com/typebotjota/sales-analytics-carros.git
cd sales-analytics-carros

# Abrir dashboard no browser
open index.html

# OU via GitHub Pages
# https://typebotjota.github.io/sales-analytics-carros/
```

---

## 📡 Pipeline de Análise por Canal

### 📞 Ligação (áudio)

```bash
# Analisar gravação de ligação
python analyze_call.py gravacao.mp3 --closer "Carlos Silva" --canal ligacao

# Com transcrição já feita
python analyze_call.py transcricao.txt --closer "Carlos Silva" --canal ligacao
```

**Fluxo:** Áudio → Whisper (transcrição) → Claude API (análise) → JSON → Dashboard

---

### 💬 WhatsApp (conversa exportada)

```bash
# Exportar chat no WhatsApp: Menu → Mais → Exportar conversa (sem mídia)
# Copiar o .txt gerado para a pasta do projeto

# Parsear e analisar
python analyze_call.py conversa_cliente.txt --closer "Rafael Santos" --canal whatsapp
```

Ou usar o parser separado:

```bash
python parse_whatsapp.py conversa_cliente.txt
```

**Métricas exclusivas WhatsApp:** tempo de primeira resposta, tempo médio, mídia enviada, follow-ups, mensagens fora do expediente.

---

### 🏪 Presencial (formulário)

```bash
# 1. Abrir formulário durante/após o atendimento
open form_presencial.html  # ou acessar no celular via rede local

# 2. Preencher e clicar "Exportar JSON" → baixa Carlos_Silva_20260303.json

# 3. Analisar com IA
python analyze_call.py Carlos_Silva_20260303.json --closer "Carlos Silva" --canal presencial
```

**Fluxo:** Formulário → JSON → Claude API (análise) → Dashboard

---

## ⚙️ Configuração (`config.json`)

```json
{
  "canais": {
    "ativos": ["ligacao", "whatsapp", "presencial"],
    "meta_semanal_por_vendedor": {
      "ligacao": 3,
      "whatsapp": 5,
      "presencial": 3
    },
    "whatsapp_thresholds_minutos": {
      "bom": 5,
      "medio": 15,
      "ruim": 30
    }
  }
}
```

---

## 📊 Exemplo de Saída (JSON analisado)

```json
{
  "id": "call-001",
  "canal": "ligacao",
  "name": "Fernando Almeida",
  "closer": "Carlos Silva",
  "score": 8.2,
  "classification": "Boa",
  "closing_probability": 75,
  "test_drive": true,
  "performance": {
    "abordagem": 9.0,
    "qualificacao": 8.5,
    "fechamento": 7.5
  },
  "top_improvements": [
    "Explorar mais o custo da inação antes do preço",
    "Criar urgência no fechamento com escassez real"
  ]
}
```

---

## 🗺️ Roadmap

### v1.0 — Concluído ✅
- [x] Dashboard com 7 views (Calls, DNA, Objeções, Relatório, Upload, Script IA, Config)
- [x] Análise de ligações via CLI
- [x] Formulário presencial mobile-first
- [x] Suporte multi-canal (ligação, WhatsApp, presencial)
- [x] Filtros por canal, vendedor e classificação
- [x] Mapa de objeções com scripts anti-objeção
- [x] Métricas específicas por canal (WPP e presencial)
- [x] Preview de conversa WhatsApp no dashboard

### v1.1 — Em Desenvolvimento 🔄
- [ ] Backend API para processar uploads diretamente no dashboard
- [ ] Integração Whisper local para transcrição offline
- [ ] Notificações WhatsApp quando análise finaliza
- [ ] Export de relatório em PDF

### v2.0 — Planejado 📋
- [ ] App mobile nativo (React Native) para formulário presencial
- [ ] Integração CRM (Pipedrive, HubSpot)
- [ ] IA preditiva: probabilidade de fechamento em tempo real
- [ ] Benchmarking entre concessionárias da rede
- [ ] Gamificação: ranking, badges, metas visuais por vendedor

---

## 🤝 Contribuição

Pull requests são bem-vindos. Para mudanças grandes, abra uma issue primeiro para discutir o que você gostaria de mudar.

---

## 📄 Licença

MIT — use, modifique e distribua livremente.
