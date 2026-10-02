# GOSPEL AI — RunPod GPU deployment

This folder defines the cloud deployment contract for the private voice inference service.

## Important

- The GitHub repository contains **code only**.
- Never commit the owner's voice recordings, OpenVoice checkpoints, API tokens, or generated private media.
- Mount the private voice profile and model directory into the container at runtime.
- The GPU service is separate from the Vercel web application.

## Container

Build from the repository root:

```bash
docker build -f backend/Dockerfile.voice -t gospel-ai-voice ./backend
```

Run with private runtime volumes:

```bash
docker run --rm -p 8000:8000 \\
  -v /data/gospel/voice_profile:/app/voice_profile:ro \\
  -v /data/gospel/models:/app/models:ro \\
  -v /data/gospel/outputs:/app/outputs \\
  -e OPENVOICE_MODEL_DIR=/app/models/openvoice_v2 \\
  -e GOSPEL_VOICE_EN=/app/voice_profile/english.wav \\
  -e GOSPEL_VOICE_FR=/app/voice_profile/french.wav \\
  -e OPENVOICE_DEVICE=cuda \\
  gospel-ai-voice
```

## Required validation

Before connecting the web application, verify:

1. `GET /api/health` returns `ok: true`.
2. `voice_runtime_available` is true.
3. Both private reference WAV files are readable.
4. The OpenVoice model files are readable.
5. A short English generation succeeds.
6. A short French generation succeeds.
7. The returned audio can be downloaded from `/audio/...`.

## Vercel connection

Set the Vite build variable:

```text
VITE_API_URL=https://YOUR_PRIVATE_VOICE_API
```

Do not put GPU credentials in Vite variables. Anything prefixed with `VITE_` is exposed to the browser.

## Cost control

Start with an on-demand GPU. Do not keep a GPU running continuously during development. Once generation is reliable, evaluate a serverless/scale-to-zero deployment if its cold-start behavior is acceptable.
