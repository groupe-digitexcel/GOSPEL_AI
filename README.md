# GOSPEL AI

**Your Voice. Your Message. Your Impact.**

GOSPEL AI is a self-hosted AI media studio designed around the owner's own voice. The first release focuses on text-to-speech, with a modular path toward narrated video.

## Architecture

- **Web UI:** React + Vite
- **API:** FastAPI
- **Voice engine:** pluggable local/self-hosted engine adapter
- **Video pipeline:** FFmpeg-ready adapter for combining generated speech with images/video
- **CI:** GitHub Actions
- **Deployment:** Vercel for the web UI; a separate Python-capable runtime is required for the inference API

## GitHub-first strategy

The public repository can use GitHub's included CI capacity for automated tests/builds. GitHub Free currently includes 2,000 Actions minutes/month for private repositories; standard runners are free for public repositories. GitHub Free also includes Codespaces quota and GitHub Pages for public repositories. These are useful for development, CI and documentation, but GitHub Actions is not intended to be the always-on GPU server for voice inference.

## Voice safety

Use only voice recordings that you own or are authorized to use. Do not configure the application to imitate another person without their permission.

## Local development

### Frontend
```bash
cd app
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open the Vite URL shown by the terminal.

## Current status

This repository is the foundation for GOSPEL AI. The UI/API contract is ready, while the actual local voice model and production inference runtime still need to be connected and tested with the owner's clean voice dataset.

## Planned media pipeline

1. Clean/validate voice samples
2. Create a local voice profile
3. Generate speech from text
4. Normalize/export audio
5. Add background music optionally
6. Combine narration with images/video
7. Export a shareable MP4
