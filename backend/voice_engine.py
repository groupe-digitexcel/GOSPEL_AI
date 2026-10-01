"""GOSPEL AI local voice engine adapter.

This adapter is intentionally local/self-hosted. It uses only the owner's
authorized reference recordings and OpenVoice V2 model files supplied on the
inference machine.
"""
from pathlib import Path
import os
from uuid import uuid4

from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
VOICE_DIR = ROOT / "voice_profile"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_DIR = Path(os.getenv("OPENVOICE_MODEL_DIR", ROOT / "models" / "openvoice_v2"))
REFERENCE_EN = Path(os.getenv("GOSPEL_VOICE_EN", VOICE_DIR / "english.wav"))
REFERENCE_FR = Path(os.getenv("GOSPEL_VOICE_FR", VOICE_DIR / "french.wav"))
DEVICE = os.getenv("OPENVOICE_DEVICE", "cpu")

_TTS = {}
_CONVERTER = None
_SE_EN = None
_SE_FR = None


def _required(path: Path, label: str):
    if not path.exists():
        raise RuntimeError(f"{label} is missing: {path}")


def _load():
    global _CONVERTER, _SE_EN, _SE_FR

    _required(MODEL_DIR, "OpenVoice model directory")
    config = MODEL_DIR / "config.json"
    checkpoint = MODEL_DIR / "checkpoint.pth"
    converter_config = MODEL_DIR / "converter" / "config.json"
    converter_checkpoint = MODEL_DIR / "converter" / "checkpoint.pth"

    for p, label in [
        (config, "OpenVoice TTS config"),
        (checkpoint, "OpenVoice TTS checkpoint"),
        (converter_config, "tone-color converter config"),
        (converter_checkpoint, "tone-color converter checkpoint"),
    ]:
        _required(p, label)

    _required(REFERENCE_EN, "English voice reference")
    _required(REFERENCE_FR, "French voice reference")

    if _CONVERTER is None:
        _CONVERTER = ToneColorConverter(str(converter_config), device=DEVICE)
        _CONVERTER.load_ckpt(str(converter_checkpoint))

    if not _TTS:
        for language in ("en", "fr"):
            _TTS[language] = BaseSpeakerTTS(str(config), device=DEVICE)
            _TTS[language].load_ckpt(str(checkpoint))

    if _SE_EN is None:
        _SE_EN, _ = se_extractor.get_se(
            str(REFERENCE_EN), _CONVERTER, vad=True
        )
    if _SE_FR is None:
        _SE_FR, _ = se_extractor.get_se(
            str(REFERENCE_FR), _CONVERTER, vad=True
        )


def generate_with_openvoice(text: str, language: str, speed: float) -> str:
    if language not in {"en", "fr"}:
        raise RuntimeError("Only English (en) and French (fr) are enabled.")

    _load()

    reference = _SE_EN if language == "en" else _SE_FR
    source = OUTPUT_DIR / f"source-{uuid4().hex}.wav"
    output = OUTPUT_DIR / f"gospel-ai-{uuid4().hex}.wav"

    _TTS[language].tts(
        text,
        str(source),
        speaker="default",
        language=language,
        speed=speed,
    )
    _CONVERTER.convert(
        audio_src_path=str(source),
        src_se=reference,
        tgt_se=reference,
        output_path=str(output),
        message="@GOSPEL_AI",
    )

    source.unlink(missing_ok=True)
    return f"/audio/{output.name}"
