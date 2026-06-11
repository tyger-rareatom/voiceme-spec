#!/usr/bin/env python3
"""
Scaffold the OpenSpec changes/ tree for VoiceMe MVP 2 + MVP 3.
Same structure as scaffold_mvp1.py. Future-phase packages carry an explicit
Status/Blocked-by header so they aren't started before prerequisites are archived.
"""
import os

ROOT = "/home/claude/voiceme/voiceme-spec/openspec/changes"

CHANGES = [
# ═════════════════════════════════ MVP 2 ═════════════════════════════════
dict(
id="mvp2-audio-gemini",
capability="audio-gemini",
proposal="""\
## Status
**Phase: MVP 2 — Blocked by:** `mvp1-audio-backend-interface`, `mvp1-tenant-config-store`,
`mvp1-usage-metering` (must be archived first).

## Why
Premium audio path: Gemini Live native audio offers the lowest per-minute cost (~$0.025/min) and
strong latency for languages it natively covers. Value driver for Scale tier is **latency + data
residency, not cost** (per-turn context re-billing makes it cost-neutral on long calls).

## What Changes
Implement Gemini Live as a second audio backend behind the `audio_backend` interface, with a
covered-language guard that prevents selecting it for unsupported languages.

## User-visible impact
Eligible tenants get a lower-latency premium voice experience; unsupported-language tenants are
prevented from a degraded configuration.

## Rollback
Route affected tenants back to `cascaded` via the config flag; no platform changes to revert.
""",
spec="""\
## ADDED Requirements

### Requirement: Gemini backend conforms to the audio interface
The system SHALL serve sessions for tenants flagged `audio_backend=gemini` via Gemini Live native
audio, passing the backend conformance suite and emitting usage to the metering plane.

#### Scenario: Gemini session served and metered
- GIVEN a tenant with audio_backend = "gemini"
- WHEN a call session starts and completes
- THEN Gemini Live serves all turns of the session
- AND a usage record is emitted with tenant_id, backend="gemini", and consumption metrics

### Requirement: Covered-language guard
The system SHALL prevent selecting the Gemini backend for a tenant whose configured language is not
natively covered by Gemini Live.

#### Scenario: Unsupported language blocked
- GIVEN a tenant whose language is Nigerian Pidgin
- WHEN an admin attempts to set audio_backend = "gemini"
- THEN the system rejects the configuration with a clear explanation
- AND suggests the cascaded or NVIDIA backend instead

### Requirement: Closed-model constraint surfaced
The system SHALL surface that custom voices and language fine-tuning are unavailable on the Gemini
backend wherever voice/persona selection is offered.

#### Scenario: Voice selection on Gemini
- GIVEN a tenant on the Gemini backend
- WHEN they open persona/voice configuration
- THEN only Gemini's fixed voice set is offered, with the constraint explained
""",
design="""\
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
""",
tasks="""\
## 1. Backend implementation
- [ ] 1.1 Gemini Live session adapter behind audio_backend interface
- [ ] 1.2 RAG context injection path (retrieval → model context)
- [ ] 1.3 Usage callback: map Gemini billing units → metering schema

## 2. Guards & conformance
- [ ] 2.1 Covered-language allowlist + flag-set and session-setup checks
- [ ] 2.2 Voice-selection constraint surfaced in portal
- [ ] 2.3 Pass audio-backend conformance suite

## 3. Validation
- [ ] 3.1 Latency benchmark vs cascaded (p50/p95, per segment)
- [ ] 3.2 Cost-per-minute measurement on real RAG-heavy calls (validate ~$0.025/min assumption)
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp2-backend-failover",
capability="failover-resilience",
proposal="""\
## Status
**Phase: MVP 2 — Blocked by:** `mvp2-audio-gemini` (a second backend must exist), `mvp1-failover-baseline`.

## Why
With two live backends, real failover becomes possible — and necessary. Gemini is a closed external
dependency; when it degrades, calls must continue on the cascaded stack rather than fail.

## What Changes
Add a failover controller that detects Gemini backend failure/degradation and fails sessions over to
the cascaded backend.

## User-visible impact
Callers experience continuity (possibly with a brief transition) instead of dropped calls during a
backend outage.

## Rollback
Failover controller disabled → baseline graceful-degradation behavior from MVP 1 applies.
""",
spec="""\
## MODIFIED Requirements

### Requirement: Audio backend failover
The system SHALL detect failure or sustained degradation of the Gemini backend and fail affected
sessions over to the cascaded backend, recording the event.

#### Scenario: Gemini outage mid-session
- GIVEN an active session on the Gemini backend
- WHEN the backend fails or exceeds degradation thresholds
- THEN the session fails over to the cascaded backend with minimal disruption
- AND the failover event is recorded in telemetry and metering (split usage attribution)

#### Scenario: New sessions during outage
- GIVEN a detected Gemini outage
- WHEN new sessions start for Gemini-flagged tenants
- THEN they are routed directly to cascaded until health recovers
""",
design="""\
## Approach
- Failover controller monitors backend health (error rate, latency SLO breach, vendor status).
- Mid-session switch: re-establish the pipeline on cascaded, carrying conversation state from the
  session runtime; accept a brief transition utterance ("one moment").
- Usage attribution splits at the failover point (metering correctness).
- Failback policy: new sessions return to Gemini after sustained health; in-flight sessions finish
  where they are.
""",
tasks="""\
## 1. Detection & control
- [ ] 1.1 Backend health monitor (error/latency/vendor signals)
- [ ] 1.2 Failover controller + failback policy

## 2. Mid-session switch
- [ ] 2.1 Conversation-state carry-over to cascaded pipeline
- [ ] 2.2 Split usage attribution at failover point

## 3. Validation
- [ ] 3.1 Chaos test: induced Gemini failure during live sessions
- [ ] 3.2 Failover telemetry + alerting
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp2-rag-vertex",
capability="rag-backend",
extra_specs=[("rag-migration", """\
## ADDED Requirements

### Requirement: Tier-upgrade content migration
The system SHALL migrate a tenant's indexed content from pgvector to Vertex AI RAG Engine on
Growth→Scale upgrade without answer-quality regression.

#### Scenario: Growth tenant upgrades to Scale
- GIVEN a Growth tenant with indexed content in pgvector
- WHEN their upgrade to Scale completes
- THEN content is re-indexed into Vertex AI RAG Engine
- AND a parity evaluation confirms retrieval quality within the agreed tolerance
- AND retrieval cuts over with zero data loss

#### Scenario: Migration failure is safe
- GIVEN a migration job that fails mid-run
- WHEN the failure occurs
- THEN retrieval continues uninterrupted on pgvector and the job can be re-run idempotently
""")],
proposal="""\
## Status
**Phase: MVP 2 — Blocked by:** `mvp1-rag-retrieval`, `mvp1-tenant-config-store`.

## Why
Scale-tier tenants need Vertex AI RAG Engine: its fixed node-hour cost amortizes at 100k+ min/month
volume, and it provides the in-region data-residency posture sovereign procurement requires.

## What Changes
Add Vertex AI RAG Engine as a second `rag_backend`, plus an idempotent tier-upgrade migration
(pgvector → Vertex) with a retrieval-parity evaluation.

## User-visible impact
Scale tenants get the residency-compliant RAG backend; upgrades migrate content without quality loss.

## Rollback
Per-tenant `rag_backend` flag back to pgvector; migration is non-destructive (source retained until
parity passes).
""",
spec="""\
## MODIFIED Requirements

### Requirement: Vertex backend behind rag_backend
The system SHALL serve retrieval for tenants flagged `rag_backend=vertex` from Vertex AI RAG Engine,
tenant-scoped, meeting the same retrieval contract as pgvector.

#### Scenario: Vertex retrieval is tenant-scoped
- GIVEN a Scale tenant on the Vertex backend
- WHEN retrieve(tenant_id, query) is called
- THEN only that tenant's chunks are returned from Vertex
- AND retrieval latency fits the live-call turn budget
""",
design="""\
## Approach
- Vertex implementation of the `rag_backend` interface; ingestion pipeline gains a Vertex indexing
  target (embedding provider per backend).
- Migration job: re-index from source documents (not from pgvector vectors) for fidelity; idempotent;
  source index retained until parity eval passes; then cutover via the config flag.
- **Region check is a hard prerequisite task:** confirm Vertex AI RAG Engine availability in the
  target region (`africa-south1` note in project.md); if unavailable, escalate — the sovereign+Vertex
  pairing has a hole and the design must be revisited.
- Cost guard: Vertex node-hours only assigned to Scale tenants (fixed-cost amortization rule).
""",
tasks="""\
## 1. Backend
- [ ] 1.1 Region availability check for Vertex AI RAG Engine (HARD GATE — do first)
- [ ] 1.2 Vertex rag_backend implementation (tenant-scoped)
- [ ] 1.3 Ingestion pipeline Vertex indexing target

## 2. Migration
- [ ] 2.1 Idempotent migration job (re-index from source docs)
- [ ] 2.2 Parity evaluation harness (pgvector ↔ Vertex, agreed tolerance)
- [ ] 2.3 Cutover + source-retention policy

## 3. Guards
- [ ] 3.1 Scale-only assignment guard (cost amortization rule)
- [ ] 3.2 Retrieval latency benchmark within turn budget
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp2-sovereign-deployment",
capability="sovereign-deployment",
proposal="""\
## Status
**Phase: MVP 2 — Blocked by:** `mvp1-tenant-provisioning`, `mvp1-observability`. Pairs with
`mvp2-isolation-hardening`.

## Why
Tier-1 banks and telcos require in-region data processing (NDPR/POPIA/SARB), customer-controlled
encryption, and auditability before they can buy. This is the Scale tier's procurement unlock.

## What Changes
Add a sovereign deployment posture: in-region VPC topology, BYOK encryption, immutable audit
logging, and a regulatory control mapping.

## User-visible impact
Regulated tenants can pass security review and contract the Scale tier.

## Rollback
Sovereign posture is per-tenant provisioning mode; standard tenants unaffected.
""",
spec="""\
## ADDED Requirements

### Requirement: Data residency
The system SHALL process and store a sovereign tenant's data exclusively within the contracted region.

#### Scenario: Sovereign tenant data stays in-region
- GIVEN a sovereign tenant contracted to a region
- WHEN audio, transcripts, documents, or vectors are processed or stored
- THEN all processing and storage occurs within that region
- AND any out-of-region dependency is either eliminated or explicitly contracted

### Requirement: BYOK encryption
The system SHALL encrypt a sovereign tenant's data at rest using the tenant's own key.

#### Scenario: Tenant key used
- GIVEN a sovereign tenant with a provided key
- WHEN their data is written at rest
- THEN encryption uses the tenant's key
- AND key revocation renders the data inaccessible

### Requirement: Immutable audit logging
The system SHALL record an immutable audit trail of administrative and data-access actions for
sovereign tenants.

#### Scenario: Admin action audited
- GIVEN a sovereign tenant
- WHEN any administrative or data-access action occurs
- THEN an append-only audit record captures actor, action, target, and timestamp
""",
design="""\
## Approach
- Per-tenant provisioning mode: sovereign tenants get in-region VPC topology (see isolation-hardening
  for dedicated compute), regional storage, and regional model endpoints where applicable.
- BYOK via cloud KMS with customer-managed keys; key-revocation path tested.
- Audit log: append-only store, tamper-evident, exportable for regulator review.
- Deliverable includes an NDPR/POPIA/SARB control mapping document (procurement artifact).

## Honest constraint
Vendor calls that cannot be made in-region (e.g., a managed LLM with no regional endpoint) must be
explicitly surfaced in the control mapping — full in-VPC inference arrives with MVP 3's NVIDIA path.
""",
tasks="""\
## 1. Topology
- [ ] 1.1 In-region VPC provisioning mode (per-tenant)
- [ ] 1.2 Regional storage + endpoint selection

## 2. Controls
- [ ] 2.1 BYOK via customer-managed KMS keys + revocation test
- [ ] 2.2 Append-only audit log + export

## 3. Compliance artifact
- [ ] 3.1 NDPR/POPIA/SARB control mapping document (with explicit out-of-region exceptions)
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp2-isolation-hardening",
capability="tenant-isolation",
proposal="""\
## Status
**Phase: MVP 2 — Blocked by:** `mvp1-tenant-provisioning`. Pairs with `mvp2-sovereign-deployment`.

## Why
A bank's security review will ask how isolation is enforced on shared infrastructure — and whether
they can have dedicated infrastructure. Assertion is not enough; enforcement must be provable.

## What Changes
Add a dedicated-isolation provisioning tier (dedicated VPC/compute for sovereign tenants),
noisy-neighbour controls on shared infra, and an isolation-proof test suite as a release gate.

## User-visible impact
Sovereign tenants get contractually dedicated infrastructure; all tenants get provable isolation.

## Rollback
Dedicated mode is per-tenant provisioning; shared-infra controls are additive.
""",
spec="""\
## MODIFIED Requirements

### Requirement: Dedicated isolation tier
The system SHALL provision sovereign tenants on dedicated VPC and compute with no shared data plane.

#### Scenario: Sovereign tenant provisioned dedicated
- GIVEN a tenant contracted for dedicated isolation
- WHEN provisioning completes
- THEN their voice runtime, RAG store, and storage run on dedicated resources
- AND no shared data-plane component carries their traffic

### Requirement: Noisy-neighbour controls on shared infrastructure
The system SHALL enforce per-tenant resource quotas and fairness on shared infrastructure so one
tenant's load cannot degrade another's latency SLO.

#### Scenario: Tenant traffic spike contained
- GIVEN tenant A spiking to its quota on shared infrastructure
- WHEN tenant B makes calls concurrently
- THEN tenant B's latency remains within SLO

### Requirement: Isolation proven by test, continuously
The system SHALL run the cross-tenant isolation suite as a release gate on every deploy.

#### Scenario: Isolation regression blocks release
- GIVEN a change that breaks tenant scoping anywhere in the stack
- WHEN the release pipeline runs
- THEN the isolation suite fails and the release is blocked
""",
design="""\
## Approach
- Provisioning modes: shared (default) vs dedicated (sovereign). Dedicated = per-tenant VPC, compute
  pool, and stores; pairs with sovereign-deployment topology.
- Shared-infra fairness: per-tenant rate/concurrency quotas at ingress; resource limits in the
  runtime; quota breaches degrade the offender, never the neighbour.
- Promote the MVP 1 cross-tenant test suite into a CI release gate; extend it to cover the new
  backends and stores as they land.
""",
tasks="""\
## 1. Dedicated tier
- [ ] 1.1 Dedicated-tenant provisioning mode (VPC + compute + stores)
- [ ] 1.2 Contract-mapping doc: what "dedicated" includes

## 2. Shared-infra fairness
- [ ] 2.1 Per-tenant quotas (rate/concurrency) at ingress
- [ ] 2.2 Runtime resource limits + breach behavior

## 3. Continuous proof
- [ ] 3.1 Isolation suite as CI release gate
- [ ] 3.2 Extend suite to Gemini/Vertex paths
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp2-scale-trial-gating",
capability="scale-trial",
proposal="""\
## Status
**Phase: MVP 2 — Blocked by:** `mvp1-usage-metering`, `mvp1-observability`, `mvp2-audio-gemini`.

## Why
Scale-tier promises (latency, language quality, cost) must be validated on the prospect's real
traffic before pricing commitments — accent/language handling in particular must be empirically
proven, not assumed.

## What Changes
Add a trial mode: time-boxed real-traffic evaluation with a measured trial report (latency, cost,
quality, deflection) and a commit gate before Scale pricing is contracted.

## User-visible impact
Prospective Scale tenants get a structured, evidence-based trial; the business avoids committing
pricing to unvalidated workloads.

## Rollback
Trial mode is a tenant state; exiting it reverts to standard onboarding.
""",
spec="""\
## ADDED Requirements

### Requirement: Real-traffic trial before Scale commitment
The system SHALL support a time-boxed trial mode for prospective Scale tenants on real traffic,
producing a measured trial report.

#### Scenario: Trial produces evidence
- GIVEN a prospect in trial mode for the agreed window
- WHEN the window closes
- THEN a trial report is generated covering latency (p50/p95), cost per conversation, answer
  quality, and deflection rate

### Requirement: Commit gate
The system SHALL require a completed trial report before a Scale-tier pricing commitment is recorded.

#### Scenario: Commitment without trial blocked
- GIVEN a prospect with no completed trial report
- WHEN a Scale contract is attempted in the system
- THEN it is blocked pending the trial gate (override requires recorded executive exception)
""",
design="""\
## Approach
- Trial = tenant state with full metering/observability on, billing off or discounted, time-boxed.
- Trial report assembled from metering + observability data; template includes the accent/language
  quality evaluation relevant to the prospect.
- Commit gate enforced in the billing/contract path; executive override is possible but recorded.
""",
tasks="""\
## 1. Trial mode
- [ ] 1.1 Trial tenant state (metering on, billing gated, time-boxed)
- [ ] 1.2 Trial report generator (latency/cost/quality/deflection)

## 2. Gate
- [ ] 2.1 Commit gate in contract path + recorded override
- [ ] 2.2 Accent/language quality eval template per prospect
""",
),
# ═════════════════════════════════ MVP 3 ═════════════════════════════════
dict(
id="mvp3-audio-nvidia",
capability="audio-nvidia",
proposal="""\
## Status
**Phase: MVP 3 — Blocked by:** `mvp1-audio-backend-interface`, `mvp1-usage-metering`,
`mvp3-gpu-ops` (deploys the serving substrate; build together).

## Why
The self-hosted NVIDIA Riva path is the substrate for the language moat (own the ASR/TTS weights →
fine-tune for Pidgin/Swahili) and completes the sovereign story (in-VPC speech processing). It only
pencils out at volume — routing must enforce the inflection rule.

## What Changes
Implement the NVIDIA backend behind `audio_backend`: Parakeet/Canary ASR + Magpie TTS served via
self-hosted NIM, with a swappable LLM slot (Claude default ⇄ Nemotron, spike-gated).

## User-visible impact
Language-pack tenants get Africa-native speech; sovereign tenants get in-VPC speech processing.

## Rollback
Per-tenant flag back to cascaded/gemini; NIM deployment torn down independently of the platform.
""",
spec="""\
## ADDED Requirements

### Requirement: NVIDIA backend conforms to the audio interface
The system SHALL serve sessions for tenants flagged `audio_backend=nvidia` via self-hosted Riva
(Parakeet/Canary ASR, Magpie TTS), passing the conformance suite and emitting usage to metering.

#### Scenario: NVIDIA session served and metered
- GIVEN a tenant with audio_backend = "nvidia"
- WHEN a call session starts and completes
- THEN Riva ASR/TTS serve the session via NIM
- AND a usage record is emitted including GPU-time attribution

### Requirement: Swappable LLM slot
The system SHALL allow the NVIDIA backend's reasoning layer to be configured per tenant as Claude
(default) or self-hosted Nemotron (only where the Nemotron spike gate has passed).

#### Scenario: Sovereign tenant on Nemotron
- GIVEN the Nemotron spike gate recorded as PASSED and a sovereign tenant requiring in-VPC inference
- WHEN their llm_slot is set to "nemotron"
- THEN reasoning runs on self-hosted Nemotron within the VPC

#### Scenario: Nemotron blocked without gate
- GIVEN the spike gate not recorded as PASSED
- WHEN an admin attempts llm_slot = "nemotron"
- THEN the configuration is rejected citing the gate

### Requirement: Volume-gated routing
The system SHALL NOT select the NVIDIA self-host backend for tenants below the self-host volume
inflection (fixed GPU cost rule).

#### Scenario: Starter tenant cannot route to self-host
- GIVEN a Starter tenant below the inflection volume
- WHEN backend selection runs
- THEN the NVIDIA backend is not selectable for that tenant (unless language-pack necessity
  explicitly overrides, recorded with cost acknowledgment)
""",
design="""\
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
""",
tasks="""\
## 1. Serving
- [ ] 1.1 Deploy Parakeet/Canary + Magpie NIMs on GPU substrate
- [ ] 1.2 NVIDIA backend impl behind audio_backend interface
- [ ] 1.3 GPU-time usage attribution → metering

## 2. LLM slot
- [ ] 2.1 llm_slot abstraction (claude | nemotron) behind LLM interface
- [ ] 2.2 Spike-gate check on nemotron selection

## 3. Routing & conformance
- [ ] 3.1 Volume-inflection routing guard (+ explicit language-necessity override)
- [ ] 3.2 Pass audio-backend conformance suite
- [ ] 3.3 Latency benchmark vs cascaded
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp3-pidgin-pack",
capability="language-pack-pidgin",
proposal="""\
## Status
**Phase: MVP 3 — Blocked by:** `mvp1-consent-capture` (data source), `mvp3-audio-nvidia` (serving
substrate). **Critical path is DATA, not code.**

## Why
Nigerian Pidgin is the language moat: closed models (Gemini) cannot host it; owning fine-tuned
ASR/TTS weights makes it defensible. Pidgin v1 (prompt-steered on cascaded) ships earlier for
demos; this change delivers Pidgin v2 — the owned pack.

## What Changes
Deliver the full pack: locked transcription style guide → labelled data acquisition (~100–300 hrs)
→ Parakeet/Canary ASR fine-tune → custom Magpie Pidgin voice → eval harness → tenant routing.

## User-visible impact
Pidgin-speaking callers get accurate recognition and a genuine Nigerian Pidgin agent voice.

## Rollback
Pidgin tenants revert to v1 (prompt-steered cascaded); fine-tuned weights are versioned and
roll back independently.
""",
spec="""\
## ADDED Requirements

### Requirement: Transcription style guide locked before labelling
The system SHALL adopt a locked Nigerian Pidgin transcription style guide before any labelling
begins, governing all training transcripts.

#### Scenario: Labelling uses the style guide
- GIVEN the locked style guide
- WHEN any audio is transcribed for training
- THEN transcripts conform to the guide (spot-check sampling enforced)

### Requirement: ASR quality bar
The fine-tuned ASR SHALL meet the agreed WER target on a held-out set of real Pidgin support calls,
improving materially over the baseline.

#### Scenario: Fine-tune evaluated on held-out calls
- GIVEN the fine-tuned Parakeet/Canary model
- WHEN evaluated on the held-out support-call set
- THEN WER meets the agreed target and beats baseline by the agreed margin
- AND failure to meet the bar blocks rollout (iterate on data, not ship)

### Requirement: Branded Pidgin voice
The agent SHALL speak with an approved Nigerian Pidgin voice produced via Magpie voice cloning,
licensed for commercial use.

#### Scenario: Voice approved and licensed
- GIVEN candidate cloned voices
- WHEN a voice is selected
- THEN native-speaker review approves naturalness and the talent license covers commercial use

### Requirement: Pidgin tenants routed to the pack
The system SHALL route Pidgin-language tenants to the NVIDIA backend with the Pidgin pack once GA.

#### Scenario: Pidgin tenant after pack GA
- GIVEN a tenant with language = Nigerian Pidgin after pack GA
- WHEN backend selection runs
- THEN the NVIDIA backend with the Pidgin pack serves them (v1 fallback retained)
""",
design="""\
## Approach — data first
- **Style guide:** commissioned with Nigerian linguist + native-speaker panel; covers orthography
  ("abeg", "wahala", code-switch conventions); locked and versioned before hour one of labelling.
- **Data sources (in order):** consented production audio via the MVP 1 consent-capture export;
  commissioned collection (support-style utterances, ~$2–4/labelled-minute); public corpora
  (AfriSpeech-style, Common Voice) as supplement. Target 100–300 labelled hours.
- **Fine-tune:** Parakeet/Canary on the corpus; held-out eval set drawn from real support calls,
  never from training data. WER target agreed with product before training starts.
- **Voice:** Magpie zero-shot from licensed Nigerian voice talent; native-speaker approval panel.
- **Eval harness:** automated intent-level eval (recognition + response quality) on real intents.

## Honest constraint
If consented production volume is thin at start, commissioned collection carries the load — budget
accordingly ($30–80k band). Do not compress the style-guide step to save time; inconsistent labels
waste the entire data budget.
""",
tasks="""\
## 1. Data (the critical path)
- [ ] 1.1 Commission + lock transcription style guide (linguist + native panel)
- [ ] 1.2 Consent-capture export pipeline → labelling queue
- [ ] 1.3 Commissioned collection contract + delivery (to 100–300 hr target)
- [ ] 1.4 Label QA sampling against style guide

## 2. Models
- [ ] 2.1 ASR fine-tune (Parakeet/Canary) + held-out WER eval
- [ ] 2.2 Magpie Pidgin voice (licensed talent, native approval)

## 3. Ship
- [ ] 3.1 Intent-level eval harness on real intents
- [ ] 3.2 Pack versioning + rollback to v1
- [ ] 3.3 Pidgin tenant routing to NVIDIA backend
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp3-swahili-pack",
capability="language-pack-swahili",
proposal="""\
## Status
**Phase: MVP 3 — Blocked by:** `mvp3-pidgin-pack` (reuses the workstream pattern + tooling),
`mvp3-audio-nvidia`.

## Why
Swahili opens the East Africa expansion (Kenya/Tanzania; M-Pesa, Safaricom, regional banks).
Second pack validates that the language-pack workstream is repeatable — the moat scales.

## What Changes
Replicate the Pidgin workstream for Swahili: style guide, data acquisition, ASR fine-tune, custom
voice, eval, regional routing.

## User-visible impact
Swahili-speaking callers get accurate recognition and a natural Swahili agent voice.

## Rollback
Swahili tenants revert to best-available covered-language backend; weights versioned.
""",
spec="""\
## ADDED Requirements

### Requirement: Swahili pack meets the same bars as Pidgin
The Swahili pack SHALL meet the same style-guide, ASR-quality, voice-approval, and eval requirements
as the Pidgin pack, with Swahili-specific targets.

#### Scenario: Swahili ASR evaluated
- GIVEN the fine-tuned Swahili ASR
- WHEN evaluated on held-out Swahili support calls
- THEN WER meets the agreed Swahili target

### Requirement: Regional routing
The system SHALL route Swahili-language tenants to the NVIDIA backend with the Swahili pack,
respecting regional residency where contracted.

#### Scenario: Kenyan tenant served regionally
- GIVEN a Kenyan tenant with language = Swahili and a regional residency contract
- WHEN sessions run
- THEN the Swahili pack serves them within the contracted region
""",
design="""\
## Approach
- Reuse the Pidgin workstream end-to-end (style-guide process, labelling pipeline, fine-tune recipe,
  voice process, eval harness) — the deliverable here is as much the *repeatable pipeline* as the pack.
- Swahili has materially more public corpus coverage than Pidgin; expect lower commissioned-data cost.
- Regional note: Kenya DPA compliance + regional serving ties into sovereign topology.
""",
tasks="""\
## 1. Data
- [ ] 1.1 Swahili style guide (reuse process)
- [ ] 1.2 Corpus assembly (public + commissioned + consented)

## 2. Models
- [ ] 2.1 ASR fine-tune + held-out eval
- [ ] 2.2 Swahili voice (licensed, native approval)

## 3. Ship
- [ ] 3.1 Eval harness on Swahili intents
- [ ] 3.2 Regional routing + Kenya DPA check
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp3-gpu-ops",
capability="gpu-ops",
proposal="""\
## Status
**Phase: MVP 3 — Blocked by:** `mvp1-observability`, `mvp1-usage-metering`. Build alongside
`mvp3-audio-nvidia`. **This is a dedicated platform workstream — not absorbable by the MVP team.**

## Why
Self-hosted NIM at production quality requires real GPU operations: deployment, concurrency-aware
autoscaling, MLOps (versioned models, rollback), and cost telemetry. Without this, the NVIDIA path
is a demo, not a tier.

## What Changes
Stand up the GPU serving substrate and its operations: NIM orchestration, autoscaling on call
concurrency, model lifecycle management, GPU cost telemetry into the margin dashboard, and the
self-host inflection routing input.

## User-visible impact
Internal; underpins NVIDIA-backend reliability, SLA, and unit economics.

## Rollback
GPU substrate is independent; tear-down reverts affected tenants to managed backends.
""",
spec="""\
## ADDED Requirements

### Requirement: Concurrency-aware autoscaling
The system SHALL autoscale GPU capacity based on concurrent call load, maintaining latency SLOs
within agreed scale-up time.

#### Scenario: Load approaches capacity
- GIVEN concurrent NVIDIA-backend calls nearing provisioned capacity
- WHEN the autoscale threshold is crossed
- THEN capacity scales up within the SLO window and no in-flight call degrades beyond SLO

### Requirement: Model lifecycle management
The system SHALL version deployed models (ASR/TTS/LLM) and support rollback without platform changes.

#### Scenario: Bad model rollback
- GIVEN a newly deployed model version causing quality regression
- WHEN rollback is triggered
- THEN the prior version serves traffic and the event is recorded

### Requirement: GPU cost telemetry
The system SHALL attribute GPU cost per tenant and per session into the metering plane and margin
dashboard.

#### Scenario: GPU cost visible per tenant
- GIVEN NVIDIA-backend traffic
- WHEN the margin dashboard is viewed
- THEN per-tenant GPU cost attribution is visible alongside vendor costs

### Requirement: Inflection routing input
The system SHALL compute per-tenant volume against the self-host inflection threshold and expose it
to the router.

#### Scenario: Tenant crosses the inflection
- GIVEN a tenant whose sustained volume crosses the threshold
- WHEN routing eligibility is recomputed
- THEN the tenant becomes eligible for self-host routing (subject to language/tier rules)
""",
design="""\
## Approach
- NIM orchestration on the chosen GPU substrate (DGX Cloud rental first; owned capex later if
  volume justifies). Concurrency model documented: streams-per-GPU by model, headroom policy.
- Autoscaling keyed to concurrent sessions (not CPU); scale-up SLO agreed with product.
- MLOps: model registry, versioned deploys, canary + rollback.
- Cost telemetry: GPU-hour attribution per session → metering schema → margin dashboard, feeding the
  inflection computation (the same number that decides A/B → C routing).

## Staffing note (binding)
This workstream requires dedicated platform engineering. The single-engineer dependency on the
platform role is a known risk — the backup reserve from the budget MUST be active before this starts.
""",
tasks="""\
## 1. Substrate
- [ ] 1.1 GPU substrate provisioning (DGX Cloud) + NIM orchestration
- [ ] 1.2 Concurrency model doc (streams/GPU, headroom)

## 2. Operations
- [ ] 2.1 Concurrency-keyed autoscaling + SLO validation
- [ ] 2.2 Model registry + versioned deploy + canary/rollback

## 3. Economics
- [ ] 3.1 GPU cost attribution → metering + margin dashboard
- [ ] 3.2 Inflection computation → router input
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp3-nemotron-spike",
capability="nemotron-llm",
proposal="""\
## Status
**Phase: MVP 3 — Blocked by:** `mvp3-gpu-ops` (serving substrate). **This change IS the gate** for
Phase 4 sovereign agentic actions and for `llm_slot=nemotron` selection.

## Why
A fully in-VPC tool-calling stack (Riva + Nemotron + Magpie) is the sovereign agentic story — but
field reports show Nemotron tool-calling is sensitive to parser/template configuration (raw-JSON
emissions, template bugs) and requires detailed-thinking-off. De-risk with a one-week spike before
any roadmap commitment depends on it.

## What Changes
Run a structured spike: serve Nemotron Super via NIM with explicit tool-call parser + chat template,
evaluate on a fixed 50-scenario tool-calling set drawn from real consented intents, against a Claude
baseline, and record a PASS/FAIL gate decision.

## User-visible impact
None directly; gates future sovereign agentic capability honestly.

## Rollback
N/A — the spike is disposable by design; only the recorded gate decision persists.
""",
spec="""\
## ADDED Requirements

### Requirement: Tool-call reliability gate
Nemotron SHALL be greenlit for sovereign agentic use only if, on the fixed 50-scenario evaluation:
tool-selection accuracy is within 5 points of the Claude baseline AND argument JSON-parse validity
is ≥ 98% AND no-tool discipline is ≥ 95% AND added latency fits the turn budget.

#### Scenario: All thresholds met
- GIVEN the completed evaluation run
- WHEN all four thresholds are met
- THEN the gate is recorded PASSED with the exact serving configuration as the supported recipe
- AND llm_slot=nemotron becomes selectable for sovereign tenants

#### Scenario: Capability passes, plumbing fails
- GIVEN tool-selection accuracy passes but JSON-parse validity fails
- WHEN the result is reviewed
- THEN parser/template remediation is time-boxed and the evaluation re-run before a final decision

#### Scenario: Capability fails
- GIVEN tool-selection or multi-step accuracy fails the thresholds
- WHEN the result is reviewed
- THEN the gate is recorded FAILED; sovereign agentic actions remain on Claude; revisit at next
  Nemotron release

### Requirement: Evaluation set realism
The 50-scenario set SHALL be drawn from real consented support intents covering: single-tool,
multi-tool selection, forced tool, no-tool discipline, and multi-step chains.

#### Scenario: Eval set composition verified
- GIVEN the assembled evaluation set
- WHEN reviewed
- THEN all five categories are represented and scenarios trace to real intents
""",
design="""\
## Approach
- Serve Nemotron Super via NIM, detailed-thinking-off, with the tool-call parser and chat template
  set explicitly (never defaults — this is where the field failures live). Pin the container version.
- Identical evaluation run against Claude as baseline; thresholds are relative (selection) and
  absolute (parse validity, discipline, latency).
- Effort: ~1 engineer, 1 week, rented GPU. The recorded decision (+ exact config on PASS) is the
  deliverable; the infrastructure is disposable.

## Gate integration
The PASS/FAIL flag is read by `mvp3-audio-nvidia`'s llm_slot guard and by the Phase 4
agentic-actions proposal as a hard prerequisite.
""",
tasks="""\
## 1. Serving
- [ ] 1.1 Nemotron Super NIM, thinking-off, explicit parser + chat template, pinned version

## 2. Evaluation
- [ ] 2.1 50-scenario set from real consented intents (5 categories)
- [ ] 2.2 Run Nemotron + Claude baseline; score 4 metrics

## 3. Decision
- [ ] 3.1 Record gate PASS/FAIL + supported config recipe
- [ ] 3.2 Wire gate flag into llm_slot guard
""",
),
]

PROPOSAL_HEADER = "# Proposal: {id}\n\n"
DESIGN_HEADER = "# Design: {id}\n\n"
TASKS_HEADER = "# Tasks: {id}\n\n"

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

count = 0
for ch in CHANGES:
    base = os.path.join(ROOT, ch["id"])
    write(os.path.join(base, "proposal.md"), PROPOSAL_HEADER.format(id=ch["id"]) + ch["proposal"])
    write(os.path.join(base, "specs", ch["capability"], "spec.md"), ch["spec"])
    for cap, spec in ch.get("extra_specs", []):
        write(os.path.join(base, "specs", cap, "spec.md"), spec)
        count += 1
    write(os.path.join(base, "design.md"), DESIGN_HEADER.format(id=ch["id"]) + ch["design"])
    write(os.path.join(base, "tasks.md"), TASKS_HEADER.format(id=ch["id"]) + ch["tasks"])
    count += 4

print(f"Wrote {count} files across {len(CHANGES)} changes under {ROOT}")
