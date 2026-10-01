# GOSPEL AI — Engine Options

## Primary: OpenVoice V2

OpenVoice V2 is the current default engine. The upstream project documents native English and French support and local installation. It uses a reference recording for voice/tone-color cloning. See the official OpenVoice documentation for the current installation/checkpoint procedure.

## Alternative A: XTTS v2

XTTS v2 is a strong fallback for English/French personal-voice synthesis. Its documented API accepts one or multiple reference WAV files and a target language. It can run locally on CPU or CUDA, although GPU is preferable for practical generation.

Suggested integration package:

```
coqui-tts
```

The exact model is:

```
tts_models/multilingual/multi-dataset/xtts_v2
```

Important: XTTS v2 uses the Coqui Public Model License, so review that license before commercial distribution.

## Alternative B: F5-TTS

F5-TTS is another local zero-shot voice-cloning research/production option. It has official code and Docker support, but its released pretrained models have a CC-BY-NC restriction according to the official repository, so it is not the default choice for a commercial product.

## Selection architecture

GOSPEL AI should expose an engine interface rather than hard-code one model:

```
VoiceEngine
  ├── OpenVoiceV2Engine
  ├── XTTSv2Engine
  └── F5TTSEngine
```

The application can then run the same smoke test against each installed engine:

Input:
"Jesus is the Savior."

Languages:
- en
- fr

Evaluation fields:
- intelligibility
- naturalness
- similarity to the authorized reference voice
- pronunciation
- latency
- memory/VRAM use
- licensing suitability

Do not automatically publish a model's output as the final production voice. The owner reviews the generated sample first.
