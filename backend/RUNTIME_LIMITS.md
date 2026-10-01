# GOSPEL AI — Runtime Limits

## Current practical limits

### Reference audio
- Personal reference recordings are currently about 2–3 minutes each.
- More reference material can improve consistency, but quality and clean speech matter more than simply increasing duration.
- Keep private voice recordings outside public Git repositories.

### OpenVoice V2
- Requires its model/checkpoint files and a Python inference environment.
- CPU inference is possible but may be slow.
- CUDA GPU is preferred for practical interactive generation.
- The web frontend should not carry the model weights.

### XTTS v2
- Official documentation lists 16 supported languages, including English and French. citeturn0search1
- It is an inference-oriented option and can use reference speech.
- Its model is under the Coqui Public Model License; commercial deployment requires reviewing that license.

### F5-TTS
- Official code supports local installation and Docker. citeturn0search0
- The official pretrained Base models are CC-BY-NC, so they are not the default commercial engine. citeturn0search5
- The official model cards include English and French variants, but model/license combinations differ. citeturn0search11

## Hardware limits

A CPU-only server can be used for development and short tests, but interactive production generation is much more practical with a compatible GPU.

A GPU server also has finite:
- VRAM
- concurrent generation capacity
- storage for model checkpoints
- monthly compute cost

The exact limits depend on the GPU/runtime selected, so we should benchmark before promising a maximum number of users or generations.

## GOSPEL AI product limits

The first release should impose:
- maximum input length
- generation timeout
- maximum concurrent jobs
- maximum output duration
- file-size limits
- authentication/rate limits
- automatic cleanup of temporary files

These are safeguards for reliability, not limits on the owner's voice archive.

## Quality limits

Voice cloning cannot guarantee perfect identity, pronunciation, emotion or accent reproduction. Results depend on:
- reference recording quality
- language
- text
- model
- inference settings
- hardware

Every engine should therefore pass the same controlled English/French test before production selection.
