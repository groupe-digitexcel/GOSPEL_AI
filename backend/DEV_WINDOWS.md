# GOSPEL AI — Windows development setup

This laptop is the development/control machine. The heavy OpenVoice inference
runtime is intentionally optional.

## 1. Check Python

Open Command Prompt:

```bat
python --version
```

The API can be developed independently of OpenVoice.

## 2. Create the API environment

From the repository root:

```bat
cd backend
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Start the API in development mode

```bat
uvicorn main_v3:app --reload --host 127.0.0.1 --port 8000
```

Open:

- http://127.0.0.1:8000/api/health
- http://127.0.0.1:8000/docs

The API should report `voice_runtime_available: false` until the dedicated
OpenVoice runtime and model files are installed.

## 4. Start the web app

In a second Command Prompt:

```bat
cd app
npm install
npm run dev
```

Vite will print the local URL.

## 5. Do not commit private voice references

Keep the owner's English/French reference recordings outside Git, or in the
ignored local directory:

```text
backend/voice_profile/english.wav
backend/voice_profile/french.wav
```

The production inference machine must provide the OpenVoice V2 model files
separately.

## 6. Production inference

Use the dedicated voice runtime described in `VOICE_RUNTIME.md`. This
Windows development setup is deliberately separated from model inference so
the application remains testable on modest hardware.
