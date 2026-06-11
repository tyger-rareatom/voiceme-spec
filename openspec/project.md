# VoiceMe — Project Foundation (`project.md`)

> This is the OpenSpec "worldview" file. It is injected into every generated artifact
> (proposals, designs, tasks). Keep it authoritative and current. Drop this into
> `openspec/project.md` after running `openspec init`.

## 1. What VoiceMe is

VoiceMe is a **multi-tenant AI voice-agent platform** that lets any African business embed a
branded customer-support voice widget on its website or mobile app via a single `<script>` tag.
Each tenant's agent is **grounded in that tenant's own documents** (RAG), goes live in under an
hour, and is billed as a **monthly subscription**. Initial beachhead: Nigerian fintech and telco.

Anchor demo tenants: **AcmePay** (fintech, agent "Sade") and **TelcoOne** (telco, agent "Tunde").

## 2. Architectural north star

One **shared platform**; the **audio runtime** and **RAG backend** are per-tenant configuration,
not forked codebases. "Swap the engine, not the car."

- **Audio runtime** is selected per tenant by an `audio_backend` flag behind a single interface:
  - **Cascaded (managed)** — LiveKit + Deepgram STT + Claude (Haiku/Sonnet routing) + Cartesia TTS. *MVP default.*
  - **Gemini Live native audio** — single closed model, cheapest/min for covered languages.
  - **Self-hosted NVIDIA Riva (NIM)** — Parakeet/Canary ASR + swappable LLM slot (Claude ⇄ Nemotron) + Magpie TTS. Owns the weights → language moat + sovereign.
- **RAG backend** is selected per tenant by a `rag_backend` flag:
  - **pgvector + Voyage** — Starter/Growth, cheap at low volume.
  - **Vertex AI RAG Engine** — Scale, amortizes at volume + in-region residency.
- **Routing rule:** language need picks audio · tier picks RAG · volume tips cascaded/Gemini → NVIDIA self-host. The router resolves backends **at session setup, not per turn** (latency budget).

## 3. Non-negotiable principles

1. **Tenant isolation is architectural, not a permission check.** Every retrieval and every
   stored object is scoped by `tenant_id`; cross-tenant access must be impossible by construction.
2. **Usage is metered from day one.** Minutes, tokens, STT/TTS seconds, and retrieval calls are
   metered per tenant in real time — this is a usage-priced business and margin leakage must be
   visible immediately, not at month-end.
3. **Voice is real-time and unforgiving.** Every backend has a defined failover path; no single
   point of failure on the live-call path.
4. **Grounded answers only.** The agent answers from the tenant's documents; hallucination surface
   is bounded by what was uploaded.
5. **Consent-governed data capture.** Production audio used for language-pack training is captured
   only with consent, with retention and redaction controls (NDPR/POPIA).
6. **Cost-routed inference.** Trivial turns → Haiku; substantive turns → Sonnet. Protect unit economics.
7. **Secure & sovereign by design.** Scale/Tier-1 tenants can run in-region (VPC) with data residency.

## 4. Tech stack (pin versions in implementation)

- **Voice/agent services:** Python 3.12, LiveKit Agents framework. FastAPI for control-plane APIs.
- **Performance-critical / DevOps services** (metering collector, media/SIP edge, telemetry): Go 1.22+ where throughput or concurrency justifies it.
- **Portal & widget:** TypeScript, Next.js (portal), a framework-free `widget.js` embed bundle.
- **Data:** PostgreSQL 16 + `pgvector`; Voyage AI embeddings (Standard); Vertex AI RAG Engine (Scale).
- **LLM:** Claude (Sonnet anchor + Haiku trivial-turn routing); self-hosted Nemotron via NIM (sovereign, spike-gated).
- **Speech:** Deepgram (STT), Cartesia (TTS) for cascaded; Gemini Live; NVIDIA Riva (Parakeet/Canary/Magpie) self-hosted.
- **Transport:** LiveKit (WebRTC); SIP trunk + WhatsApp Business adapters via a channel-ingress layer.
- **Cloud:** GCP primary. Region note: GCP's nearest African region is `africa-south1` (Johannesburg) — farther from Lagos; validate latency for the Nigerian beachhead and confirm Vertex RAG Engine regional availability.
- **Billing:** Stripe (subscription + metered overage).
- **Infra/DevOps:** Infrastructure-as-Code (Terraform), containerized (Docker), CI/CD with automated tests, GPU orchestration for NIM (Year 1+). Observability first-class (metrics, traces, logs, per-tenant dashboards).

## 5. Architecture patterns & code standards

- **Service boundaries:** control plane (portal, config, billing, metering) is separate from the
  data/voice plane (live-call runtime). Backend selection is a runtime concern resolved by the
  Tenant Config Router at session start.
- **Backend abstraction:** the `audio_backend` and `rag_backend` interfaces are stable contracts;
  concrete backends are plugins. New backends must not require changes to the shared platform.
- **All tenant data access goes through a tenant-scoped repository layer** that requires `tenant_id`;
  direct unscoped queries are forbidden.
- **Every external vendor is swappable.** No business logic may hard-depend on a single vendor's SDK
  surface; wrap vendors behind internal interfaces.
- **Tasks must be atomic** (implementable by an agent without further clarification; ~2-hour chunks).
- **Specs use Given/When/Then scenarios.** Proposals state user-visible impact and rollback strategy.

## 6. Phase map (build order)

- **MVP 1 — Standard platform GA** (Months 1–5): multi-tenant platform, cascaded audio, RAG + continuous ingestion, widget, billing, **metering**, **basic failover**, escalation + CRM, consent capture, channel-ingress abstraction.
- **MVP 2 — Premium / Scale tier + sovereign** (Months 5–9): Gemini Live backend + B→A fallback, Vertex RAG + tier-upgrade migration, sovereign deployment, isolation hardening, trial-gating.
- **MVP 3 — Africa language moat** (Year 1–2): NVIDIA self-host backend, Pidgin & Swahili language packs, GPU ops, Nemotron LLM slot + tool-calling spike gate.
- **Phase 4 — Agentic actions & intelligence** (Year 2): function-calling actions, conversation intelligence, outbound campaigns (compliance-gated), context-rich live-agent handoff.
- **Phase 5 — Scale & expansion** (Year 2+): self-hosted-LLM volume migration, vertical knowledge templates, compliance certifications as product, integration marketplace, multi-region, developer platform.

## 7. Commercial guardrails (constrain technical choices)

- Operative pricing card is the **enterprise** tier set ($2–5k Starter / $10–20k Growth / $30–60k Scale),
  which is margin-positive. The $99/$499 placeholder pricing is **discarded** (margin-negative).
- Gemini Live is **cost-neutral, not cheaper** on long calls (per-turn context re-billing); its Scale-tier
  value is **latency + data residency**, not cost.
- Self-host (NVIDIA/Nemotron) only pencils out **above the volume inflection (~60k conversations/mo per tenant)** —
  never route Starter tenants to dedicated GPU.
- **Metering precision gates billing integrity.** Treat per-tenant usage accuracy as a correctness requirement.

## 8. Open risks the specs must keep visible

- Claude per-minute cost ($/min) is the most fragile unit-economics input — load-test to settle.
- Language packs require **labelled Pidgin/Swahili audio data** (the true critical path), not just model access.
- Nemotron tool-calling reliability is **spike-gated** before any sovereign agentic-actions commitment.
- Single-engineer dependency risk on the platform/GPU role — staff a backup.
