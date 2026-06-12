# Design: mvp1-audio-cascaded

## Approach
- LiveKit Agents (Python) orchestrates STT/LLM/TTS. Each vendor sits behind an internal interface
  (swappable: no business logic may depend on a vendor SDK surface).
- LLM router classifies turn complexity (target mix ~Haiku 30% / Sonnet 70%).
- Conversation/turn state held in the session runtime; VAD-driven turn-taking and barge-in owned here.

## Hosting & vendor placement (MVP-1 decision)
- The cascaded runtime runs in **GCP `europe-west3` (Frankfurt)**; LiveKit agents in **`eu-central`**.
- **All vendors pinned to their EU endpoints** so no live turn crosses the Atlantic:
  - Deepgram STT → `api.eu.deepgram.com` · Cartesia TTS → EU region · Claude → Vertex AI EU (Frankfurt)
  - retrieval embeddings → Vertex `gemini-embedding-001` EU (see `mvp1-knowledge-ingestion`).
- **Rationale:** one region serves both the SA and Nigerian markets; collapses the 4 transatlantic vendor
  hops a US-hosted cascaded stack would incur down to **zero**; gives an EU/GDPR residency posture. The only
  ocean-ish leg is a single user→Frankfurt media hop (cushioned by LiveKit's edge mesh). See `project.md` §2.
- Weakest leg is **Joburg→Frankfurt (~150-180ms)**; if SA UX disappoints, the first lever is a LiveKit
  African media-edge, **not** a region move.

## Hot-path sequence note
audio in → VAD/turn detect → STT → (retrieve) → LLM (routed) → TTS → audio out. Each segment is
instrumented separately for the latency budget and metering. With EU-pinned vendors the estimated
end-to-end (end-of-speech → first audio) is **~1.2-1.6s** — load-test to confirm; the structural win
(zero transatlantic vendor hops) is the robust claim, the exact ms are not.

## Validation spikes (gate launch)
- [ ] **Deepgram Nigerian-accented-English WER** on real support audio — the MVP-1 *language* gate.
      SA-English is safe on base models; Nigerian English is the risk. If WER is poor → prompt-steer
      harder / flag Pidgin handling as a known MVP-1 limitation, not an architecture change.
- [ ] **Joburg→Frankfurt live latency probe** — confirm the SA media leg holds at Frankfurt.
