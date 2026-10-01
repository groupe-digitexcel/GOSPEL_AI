from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from voice_engine import generate_with_openvoice

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(title="GOSPEL AI API", version="0.3.0")
app.mount("/audio", StaticFiles(directory=str(OUTPUT_DIR)), name="audio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    language: str = Field(default="en", pattern="^(en|fr)$")
    speed: float = Field(default=1.0, ge=0.7, le=1.3)

@app.get("/api/health")
def health():
    return {"ok": True, "service": "gospel-ai", "voice_engine": "openvoice-v2-local"}

@app.post("/api/generate")
def generate(request: GenerateRequest):
    try:
        return {
            "ok": True,
            "audio_url": generate_with_openvoice(
                request.text, request.language, request.speed
            ),
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
