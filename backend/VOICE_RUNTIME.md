# GOSPEL AI Voice Runtime

## Runtime contract

This container is the inference service, not the Vercel web frontend.

Required runtime files:

- `voice_profile/english.wav`
- `voice_profile/french.wav`
- OpenVoice V2 model files under `models/openvoice_v2/`

Recommended deployment target: a Python 3.11 machine with NVIDIA CUDA GPU when available.

## Build

```bash
docker build -f Dockerfile.voice -t gospel-ai-voice .
```

## Run

```bash
docker run --rm -p 8000:8000 \
  -v "$PWD/voice_profile:/app/voice_profile:ro" \
  -v "$PWD/models:/app/models:ro" \
  -v "$PWD/outputs:/app/outputs" \
  -e OPENVOICE_MODEL_DIR=/app/models/openvoice_v2 \
  -e GOSPEL_VOICE_EN=/app/voice_profile/english.wav \
  -e GOSPEL_VOICE_FR=/app/voice_profile/french.wav \
  -e OPENVOICE_DEVICE=cpu \
  gospel-ai-voice
```

For a CUDA runtime, use a CUDA-compatible PyTorch installation and set `OPENVOICE_DEVICE=cuda`.

## First smoke test

After the service starts:

```bash
curl http://localhost:8000/api/health
```

Then send a short English generation request to `/api/generate`.

Do not put private voice recordings or model credentials in Git. Keep them mounted through the runtime environment.
