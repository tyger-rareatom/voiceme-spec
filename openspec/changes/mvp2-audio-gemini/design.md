# Design: mvp2-audio-gemini

## Approach
- Implement behind the `audio_backend` interface; reuse the turn-taking/session abstraction from the
  cascaded backend where the native-audio model allows (turn semantics differ — document the diff).
- Covered-language allowlist maintained in config; checked at flag-set time AND at session setup
  (defense in depth — the allowlist can change).
- Usage callback maps Gemini billing units (audio-in/audio-out/text tokens) into the metering schema.

## Cost note (binding)
Audio-output tokens (~$12/M) are the dominant cost lever and the most volatile price. Re-verify the
rate card before GA and meter audio-out tokens explicitly so margin per tenant is observable.

## Hot-path sequence note
Native audio collapses STT/LLM/TTS into one model call; segment instrumentation becomes
{transport, model, retrieval}. Latency budget target unchanged (≤1.5s p50; expect better).
