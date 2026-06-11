# Design: mvp3-audio-nvidia

## Approach
- Riva ASR/TTS served as NIM on the GPU substrate from `mvp3-gpu-ops`; backend implements the
  audio interface with GPU-time usage attribution flowing to metering and the margin dashboard.
- LLM slot abstraction: same internal LLM interface as cascaded; "claude" (API) and "nemotron"
  (in-VPC NIM) implementations. Nemotron selectable only when the spike gate flag is PASSED.
- Routing: inflection rule enforced in the router (volume + tier check); language-pack necessity
  override exists but is explicit and cost-acknowledged.

## Hot-path sequence note
audio → Riva ASR (in-VPC) → retrieve → LLM (slot) → Magpie TTS (in-VPC) → audio. Target same ≤1.5s
p50; GPU locality should help ASR/TTS segments.
