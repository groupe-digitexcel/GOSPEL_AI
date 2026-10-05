"""GOSPEL AI OpenVoice V2 inference adapter.

Uses the official OpenVoice V2 pipeline:
MeloTTS -> source speaker embedding -> ToneColorConverter -> authorized target voice.
Only the owner's private reference recordings are used.
"""
from pathlib import Path
import os
from uuid import uuid4

import torch
from melo.api import TTS
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
VOICE_DIR = ROOT / "voice_profile"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_DIR = Path(os.getenv("OPENVOICE_MODEL_DIR", ROOT / "models" / "checkpoints_v2"))
REFERENCE_EN = Path(os.getenv("GOSPEL_VOICE_EN", VOICE_DIR / "english.wav"))
REFERENCE_FR = Path(os.getenv("GOSPEL_VOICE_FR", VOICE_DIR / "french.wav"))
DEVICE = os.getenv("OPENVOICE_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")

# Official OpenVoice V2 base-speaker identifiers.
BASE_LANGUAGE = {"en": "EN_NEWEST", "fr": "FR"}
BASE_SPEAKER = {
    "en": os.getenv("OPENVOICE_EN_SPEAKER", "en-newest"),
    "fr": os.getenv("OPENVOICE_FR_SPEAKER", "fr"),
}

_CONVERTER = None
_TARGET_SE = {}
_TTS = {}
_SOURCE_SE = {}


def _required(path: Path, label: str):
    if not path.exists():
        raise RuntimeError(f"{label} is missing: {path}")


def _speaker_checkpoint(language: str) -> Path:
    path = MODEL_DIR / "base_speakers" / "ses" / f"{BASE_SPEAKER[language]}.pth"
    _required(path, f"{language} base speaker embedding")
    return path


def _load():
    global _CONVERTER

    converter_config = MODEL_DIR / "converter" / "config.json"
    converter_checkpoint = MODEL_DIR / "converter" / "checkpoint.pth"

    _required(MODEL_DIR, "OpenVoice V2 model directory")
    _required(converter_config, "OpenVoice V2 converter config")
    _required(converter_checkpoint, "OpenVoice V2 converter checkpoint")
    _required(REFERENCE_EN, "English voice reference")
    _required(REFERENCE_FR, "French voice reference")

    if _CONVERTER is None:
        _CONVERTER = ToneColorConverter(str(converter_config), device=DEVICE)
        _CONVERTER.load_ckpt(str(converter_checkpoint))

    refs = {"en": REFERENCE_EN, "fr": REFERENCE_FR}
    for language, ref in refs.items():
        if language not in _TARGET_SE:
            _TARGET_SE[language], _ = se_extractor.get_se(
                str(ref), _CONVERTER, vad=True
            )

    for language in ("en", "fr"):
        if language not in _TTS:
            _TTS[language] = TTS(
                language=BASE_LANGUAGE[language],
                device=DEVICE,
            )

        if language not in _SOURCE_SE:
            _SOURCE_SE[language] = torch.load(
                _speaker_checkpoint(language),
                map_location=DEVICE,
            )


def generate_with_openvoice(text: str, language: str, speed: float) -> str:
    if language not in {"en", "fr"}:
        raise RuntimeError("Only English (en) and French (fr) are enabled.")

    _load()

    model = _TTS[language]
    speaker_ids = model.hps.data.spk2id
    requested = BASE_SPEAKER[language]

    # MeloTTS speaker IDs may use underscores while the checkpoint filenames
    # use hyphens. Resolve case-insensitively.
    speaker_id = None
    for key, value in speaker_ids.items():
        normalized = key.lower().replace("_", "-")
        if normalized == requested.lower():
            speaker_id = value
            break

    if speaker_id is None:
        raise RuntimeError(
            f"MeloTTS speaker '{requested}' is unavailable. "
            f"Available speakers: {', '.join(speaker_ids.keys())}"
        )

    source = OUTPUT_DIR / f"source-{uuid4().hex}.wav"
    output = OUTPUT_DIR / f"gospel-ai-{uuid4().hex}.wav"

    model.tts_to_file(
        text,
        speaker_id,
        str(source),
        speed=speed,
    )

    _CONVERTER.convert(
        audio_src_path=str(source),
        src_se=_SOURCE_SE[language],
        tgt_se=_TARGET_SE[language],
        output_path=str(output),
        message="@GOSPEL_AI",
    )

    source.unlink(missing_ok=True)
    return f"/audio/{output.name}"
