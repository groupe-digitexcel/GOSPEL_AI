# GOSPEL AI — Voice Engine Setup

The web app and the voice inference runtime are separate by design.

## 1. Voice references

Copy the two authorized recordings into:

- `backend/voice_profile/english.wav`
- `backend/voice_profile/french.wav`

Do not commit private voice recordings to a public repository.

## 2. OpenVoice V2

Install `requirements-voice.txt` on the Python machine that will perform inference.

Set:

```text
OPENVOICE_MODEL_DIR=/absolute/path/to/openvoice_v2
OPENVOICE_DEVICE=cuda
GOSPEL_VOICE_EN=/absolute/path/to/english.wav
GOSPEL_VOICE_FR=/absolute/path/to/french.wav
```

Use `OPENVOICE_DEVICE=cpu` when a GPU is unavailable, understanding that generation will be slower.

The model directory must contain the OpenVoice V2 TTS configuration/checkpoint and tone-color-converter configuration/checkpoint expected by `voice_engine.py`.

## 3. Start the API

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-voice.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 4. Connect the API

Set the frontend's `VITE_API_URL` to the URL of this Python inference API.

The frontend itself can be hosted on Vercel. The heavy voice model should run on a Python-capable machine.

## Privacy

Only use voice recordings that you own or are authorized to use.
