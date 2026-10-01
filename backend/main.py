from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = APP_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(title="GOSPEL AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    language: str = Field(default="en")
    speed: float = Field(default=1.0, ge=0.7, le=1.3)


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "service": "gospel-ai",
        "voice_engine": "adapter-not-connected",
        "video_pipeline": "planned",
    }


@app.post("/api/generate")
def generate(request: GenerateRequest):
    try:
        audio_url = generate_with_voice_engine(
            text=request.text,
            language=request.language,
            speed=request.speed,
        )
        return {"ok": True, "audio_url": audio_url}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


def generate_with_voice_engine(text: str, language: str, speed: float) -> str:
    """
    Integration point for the self-hosted voice engine.

    Only the owner's authorized voice dataset should be used here.
    The production implementation will load the local voice profile,
    synthesize the requested text, normalize the output and return
    a media URL.
    """
    raise RuntimeError(
        "Voice engine is not connected yet. Add the authorized local voice "
        "model and inference runtime before generating audio."
    )


# Future media endpoint:
# POST /api/video -> narration + images/video + FFmpeg export -> MP4
