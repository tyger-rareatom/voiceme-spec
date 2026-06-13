# Design: mvp1-llm-routing-spike

## Approach
- Three-way evaluation: **Gemma 4 26B A4B (Vertex EU)** vs **Claude Haiku 4.5** (the cost incumbent) vs
  **Claude Sonnet** (quality gold standard + the bar for "substantive" turns).
- **Frozen ~120-scenario set** from anchor-tenant docs, across categories that map to real design surfaces:
  grounded-answerable (40), out-of-scope/no-context (20), tool-requiring (20), no-tool-needed (10),
  escalation-warranted (15), multilingual/code-switch — SA-English/Nigerian-English/light Pidgin (15),
  adversarial/safety incl. doc-borne prompt-injection (10).
- Thresholds are relative (vs Sonnet/Haiku) and absolute (safety floors). The recorded verdict + the
  frozen suite are the deliverables; serving is Vertex-EU serverless, so no GPU and no infra to keep.
- Effort: ~1 engineer, ~1 week.

## Rigor controls (validity-critical)
- **Identical retrieved context fed to all three models** per scenario — we test the brain, holding RAG
  fixed (no retrieval variance confound).
- **STT-style input, not clean text** — disfluencies, no punctuation, accent artifacts — because that is
  what the LLM actually receives in the live pipeline.
- Blind LLM-judge (Opus) on grounding/quality with answer-order randomized; human spot-check on a
  stratified sample of every category. Function-call / escalation scored deterministically vs labels.
- Fixed shipping temperature; report variance over ≥3 runs. Same system prompt across models (minimal
  per-format adaptation only).
- Voice-appropriateness checked: concise, no markdown, speakable (TTS a sample).

## Metrics → verdict
- Hard floor for ANY production routing: grounding/faithfulness ≥98% no-hallucination, refusal
  correctness ≥95%, safety set clean.
- Function-call gate (selection within 5 pts of Claude · JSON-valid ≥98% · no-tool discipline ≥95%) is
  **identical to the Nemotron gate** by design — a Gemma pass here pre-clears sovereign agentic actions.
- Escalation false-negative rate ≤3% (missing an escalation is the dangerous error).
- Verdict B (Gemma takes substantive turns) requires grounding + answer-quality within ~3 pts of Sonnet;
  Verdict C (cheap tier only) requires beating/tying Haiku at a lower absolute bar.

## Pidgin base-vs-tuned readout
- The multilingual slice MUST include a genuine Nigerian-Pidgin subset (not just light code-switch),
  scored for base Gemma against the grounding/quality floor. Output an explicit verdict: **base adequate**
  (no tune; bank the saving) or **gap** (a Pidgin LoRA adapter is warranted).
- A "gap" verdict does NOT auto-trigger a tune: a tuned Gemma is a *deployed* endpoint (ongoing cost,
  unlike serverless base), so the adapter is built only when a channel can deliver its value — a text
  channel (full value) or MVP-3 speech models (voice). Measure now; tune when both gap AND channel exist.

## Gate integration
- The recorded verdict sets the LLM router's tier map in `mvp1-audio-cascaded` (which model serves
  trivial vs substantive vs hard/escalation turns).
- The Pidgin verdict gates whether the brain-layer language workstream in `mvp3-pidgin-pack` starts
  early (and whether it splits BRAIN/text from SPEECH/audio).
- The frozen set + harness become the reusable **LLM acceptance suite** — reused for the MVP-3
  managed→self-hosted Gemma parity check, future model upgrades, and (its function-call portion) the
  sovereign agentic gate referenced by `mvp3-nemotron-spike`.
