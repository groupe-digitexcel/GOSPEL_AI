from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Keep the API usable on the development PC even when the heavy voice
# runtime/model is not installed yet. The inference dependency is loaded
# only when /api/generate is actually called.
VOICE_IMPORT_ERROR = None
try:
    from voice_engine import generate_with_openvoice
except Exception as exc:  # pragma: no cover - depends on optional runtime
    generate_with_openvoice = None
    VOICE_IMPORT_ERROR = f"{type(exc).__name__}: {exc}"

app = FastAPI(title="GOSPEL AI API", version="0.4.0")
app.mount("/audio", StaticFiles(directory=str(OUTPUT_DIR)), name="audio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    language: str = Field(default="en", pattern="^(en|fr)$")
    speed: float = Field(default=1.0, ge=0.7, le=1.3)


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "service": "gospel-ai",
        "api_version": "0.4.0",
        "voice_engine": "openvoice-v2-local",
        "voice_runtime_available": generate_with_openvoice is not None,
    }


@app.post("/api/generate")
def generate(request: GenerateRequest):
    if generate_with_openvoice is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "The OpenVoice runtime is not installed on this machine yet. "
                "The GOSPEL AI API is running, but voice inference requires "
                "the dedicated voice runtime and model files."
            ),
        )

    try:
        return {
            "ok": True,
            "audio_url": generate_with_openvoice(
                request.text, request.language, request.speed
            ),
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
