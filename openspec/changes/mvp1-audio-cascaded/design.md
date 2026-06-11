# Design: mvp1-audio-cascaded

## Approach
- LiveKit Agents (Python) orchestrates STT/LLM/TTS. Each vendor sits behind an internal interface
  (swappable: no business logic may depend on a vendor SDK surface).
- LLM router classifies turn complexity (target mix ~Haiku 30% / Sonnet 70%).
- Conversation/turn state held in the session runtime; VAD-driven turn-taking and barge-in owned here.

## Hot-path sequence note
audio in → VAD/turn detect → STT → (retrieve) → LLM (routed) → TTS → audio out. Each segment is
instrumented separately for the latency budget and metering.
