# Sales Analytics Pro — API Backend
# FastAPI server para análise ao vivo (Amostra Grátis do demo)
# Deploy: Railway (Dockerfile)

import json
import os
import tempfile
from datetime import datetime

import anthropic
import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analyze_call import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_WHATSAPP,
    _clean_json,
)
from parse_whatsapp import parse_whatsapp

# ─── Config ──────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-6"
GROQ_WHISPER_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_WHISPER_MODEL = "whisper-large-v3-turbo"
AUDIO_EXTENSIONS = {".mp3", ".mp4", ".m4a", ".wav"}
MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB

# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(title="Sales Analytics Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Helpers ─────────────────────────────────────────────────────────────────


def _call_claude(system_prompt: str, user_content: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    raw = message.content[0].text
    return json.loads(_clean_json(raw))


async def _transcribe_groq(audio_path: str) -> str:
    """Transcreve áudio usando Groq Whisper API."""
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    filename = os.path.basename(audio_path)
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            GROQ_WHISPER_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            files={"file": (filename, audio_bytes, "audio/mpeg")},
            data={"model": GROQ_WHISPER_MODEL, "language": "pt"},
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Groq Whisper error {response.status_code}: {response.text}",
        )

    return response.json()["text"]


def _build_analysis_id(canal: str) -> str:
    return f"{canal}-amostra-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def _parse_whatsapp_from_text(text: str) -> dict:
    """Escreve texto em arquivo temporário e chama parse_whatsapp."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(text)
        tmp_path = tmp.name
    try:
        return parse_whatsapp(tmp_path)
    finally:
        os.unlink(tmp_path)


def _analyze_whatsapp_parsed(parsed: dict, closer: str) -> dict:
    metricas = parsed["metricas"]
    metricas_txt = "\n".join(f"  {k}: {v}" for k, v in metricas.items())

    user_content = (
        f"Analise esta conversa de vendas automotivas via WhatsApp.\n\n"
        f"Vendedor identificado: {parsed['vendedor']}\n"
        f"Cliente identificado: {parsed['cliente']}\n"
        f"Data de referencia: {datetime.now().strftime('%Y-%m-%d')}\n"
        f"Duracao total da conversa: {parsed['duration']}\n\n"
        f"METRICAS OBJETIVAS (pre-calculadas):\n{metricas_txt}\n\n"
        f"CONVERSA:\n{parsed['conversa_texto']}"
    )

    analysis = _call_claude(SYSTEM_PROMPT_WHATSAPP, user_content)
    analysis["id"] = _build_analysis_id("whatsapp")
    analysis["canal"] = "whatsapp"
    analysis["closer"] = closer or parsed["vendedor"]
    analysis["date"] = datetime.now().strftime("%Y-%m-%d")
    analysis["duration"] = parsed["duration"]
    analysis["canal_data"] = metricas
    return analysis


# ─── Endpoints ───────────────────────────────────────────────────────────────


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    closer: str = Form(...),
    canal: str = Form(...),
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
):
    """
    Analisa ligação (áudio) ou conversa WhatsApp (arquivo .txt ou texto colado).
    """
    if canal not in ("ligacao", "whatsapp"):
        raise HTTPException(status_code=400, detail="canal deve ser 'ligacao' ou 'whatsapp'")

    # ── Ligação ──────────────────────────────────────────────────────────────
    if canal == "ligacao":
        if file is None:
            raise HTTPException(status_code=400, detail="Envie o arquivo de áudio para canal=ligacao")

        suffix = os.path.splitext(file.filename or "")[1].lower()
        if suffix not in AUDIO_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Formato não suportado. Use: {', '.join(AUDIO_EXTENSIONS)}",
            )

        content = await file.read()
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="Arquivo maior que 25 MB")

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            transcription = await _transcribe_groq(tmp_path)
        finally:
            os.unlink(tmp_path)

        user_content = (
            f"Analise esta call de venda automotiva.\n\n"
            f"Vendedor: {closer}\n"
            f"Data: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            f"TRANSCRICAO:\n{transcription}"
        )
        analysis = _call_claude(SYSTEM_PROMPT, user_content)
        analysis["id"] = _build_analysis_id("ligacao")
        analysis["canal"] = "ligacao"
        analysis["closer"] = closer
        analysis["date"] = datetime.now().strftime("%Y-%m-%d")
        analysis["canal_data"] = None
        return analysis

    # ── WhatsApp ─────────────────────────────────────────────────────────────
    if file is not None:
        content = await file.read()
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="Arquivo maior que 25 MB")
        wpp_text = content.decode("utf-8", errors="replace")
    elif text:
        wpp_text = text
    else:
        raise HTTPException(
            status_code=400,
            detail="Envie arquivo .txt ou o campo 'text' para canal=whatsapp",
        )

    try:
        parsed = _parse_whatsapp_from_text(wpp_text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return _analyze_whatsapp_parsed(parsed, closer)


class AnalyzeTextRequest(BaseModel):
    text: str
    closer: str


@app.post("/analyze-text")
def analyze_text(body: AnalyzeTextRequest):
    """Análise de conversa WhatsApp colada como texto (JSON body)."""
    try:
        parsed = _parse_whatsapp_from_text(body.text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return _analyze_whatsapp_parsed(parsed, body.closer)
