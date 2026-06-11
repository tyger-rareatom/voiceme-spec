#!/usr/bin/env python3
"""
Scaffold the OpenSpec changes/ tree for VoiceMe MVP 1.
Generates openspec/changes/<change-id>/{proposal.md, specs/<capability>/spec.md, design.md, tasks.md}
Re-runnable: overwrites existing files (keep this script as the source of truth alongside the master spec).
"""
import os, textwrap

ROOT = "/home/claude/voiceme/voiceme-spec/openspec/changes"

CHANGES = [
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-tenant-provisioning",
capability="tenant-provisioning",
proposal="""\
## Why
Every other capability depends on a tenant existing and being isolated. This is the root change.

## What Changes
Add self-serve sign-up, auth, branded subdomain provisioning, and a tenant-scoped data model with
role-based access (admin/member).

## User-visible impact
A business can create an account and receive an isolated, branded workspace.

## Rollback
Feature-flag sign-up closed; existing tenants unaffected (additive schema only).
""",
spec="""\
## ADDED Requirements

### Requirement: Self-serve tenant sign-up
The system SHALL allow a business to create a tenant account with email verification and provision
an isolated workspace identified by a unique `tenant_id`.

#### Scenario: New business signs up
- GIVEN a visitor with a valid business email
- WHEN they complete sign-up and verify their email
- THEN a tenant is created with a unique `tenant_id` and a branded subdomain is provisioned
- AND the visitor becomes the tenant's first admin user

### Requirement: Tenant isolation by construction
The system SHALL scope every stored object and data access by `tenant_id` such that no request
authenticated for tenant A can read or write tenant B's data.

#### Scenario: Cross-tenant access is impossible
- GIVEN an authenticated user of tenant A
- WHEN they request a resource belonging to tenant B (by id or by crafted query)
- THEN the system returns not-found/forbidden and logs the attempt
- AND no tenant B data is exposed

### Requirement: Role-based access within a tenant
The system SHALL support at least admin and member roles per tenant.

#### Scenario: Member cannot change billing
- GIVEN a member (non-admin) user
- WHEN they attempt to change the subscription tier
- THEN the action is denied
""",
design="""\
## Approach
- Control-plane service (FastAPI). Postgres with a `tenants` table and a **tenant-scoped repository
  layer** that requires `tenant_id` on every query; unscoped queries forbidden by lint/review.
- Subdomain provisioning via wildcard DNS + per-tenant routing.
- Auth via OIDC-compatible provider; sessions carry `tenant_id` + role claims.

## Tenant-isolation note
Isolation is enforced at the repository layer by construction (required parameter), backed by a
cross-tenant test suite that must prove inaccessibility — not by per-endpoint permission checks alone.
""",
tasks="""\
## 1. Schema & isolation foundation
- [ ] 1.1 Create tenants + users schema with tenant_id FKs
- [ ] 1.2 Implement tenant-scoped repository base class (requires tenant_id)
- [ ] 1.3 Cross-tenant access test suite (must prove isolation)

## 2. Sign-up & access
- [ ] 2.1 Sign-up + email verification flow
- [ ] 2.2 Wildcard-subdomain provisioning + routing
- [ ] 2.3 Role model (admin/member) + authorization middleware
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-knowledge-ingestion",
capability="knowledge-ingestion",
proposal="""\
## Why
The continuous-learning RAG pipeline is the core differentiator ("the agent learns within the hour").

## What Changes
Add document upload (PDF/DOCX/Markdown/URL), chunking, embedding, indexing, and re-index on update.

## User-visible impact
A tenant uploads FAQs/how-tos/product docs; the agent reflects them shortly after.

## Rollback
Disable ingestion endpoint; existing indexes remain queryable.
""",
spec="""\
## ADDED Requirements

### Requirement: Multi-format document ingestion
The system SHALL accept PDF, DOCX, Markdown, and web URLs, chunk them, embed the chunks, and index
them in the tenant's RAG store scoped by `tenant_id`.

#### Scenario: Tenant uploads an FAQ PDF
- GIVEN an authenticated tenant admin
- WHEN they upload an FAQ PDF
- THEN the document is chunked, embedded via the configured embedding provider, and indexed
- AND the chunks are tagged with the tenant_id and source metadata

### Requirement: Continuous re-index on update
The system SHALL re-index changed documents so updates are reflected within one hour.

#### Scenario: FAQ is updated
- GIVEN a previously ingested document
- WHEN the tenant uploads a new version
- THEN stale chunks are replaced and retrieval reflects the new content within one hour
""",
design="""\
## Approach
- Ingestion worker (async queue). Chunker → embeddings (Voyage for Standard tier) → pgvector upsert.
- Idempotent re-index keyed by document hash; soft-delete superseded chunks.
- Embedding provider behind an interface (Voyage now; Vertex path arrives in MVP 2).

## Hot-path note
Ingestion is off the live-call path; no latency budget interaction. Status surfaced asynchronously.
""",
tasks="""\
## 1. Intake
- [ ] 1.1 Upload endpoint + storage (PDF/DOCX/MD/URL fetchers)
- [ ] 1.2 Chunker with source metadata

## 2. Index
- [ ] 2.1 Embedding provider interface + Voyage implementation
- [ ] 2.2 pgvector upsert + tenant scoping
- [ ] 2.3 Re-index on update (hash-keyed, idempotent)

## 3. Surface
- [ ] 3.1 Ingestion status surfaced in portal
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-rag-retrieval",
capability="rag-retrieval",
proposal="""\
## Why
Grounded answers require tenant-scoped retrieval in the live-call hot path.

## What Changes
Add a retrieval API returning top-k chunks for a query, scoped by tenant, behind the `rag_backend`
interface (pgvector first).

## User-visible impact
The agent answers from the tenant's own content only; admits when it doesn't know.

## Rollback
Additive; retrieval can be bypassed per tenant via flag for debugging.
""",
spec="""\
## ADDED Requirements

### Requirement: Tenant-scoped retrieval
The system SHALL expose `retrieve(tenant_id, query)` returning top-k chunks for that tenant only.

#### Scenario: Retrieval never crosses tenants
- GIVEN tenants A and B with distinct documents
- WHEN retrieve(A, query) is called
- THEN only tenant A chunks are returned, regardless of query content

### Requirement: Grounded-answer bounding
The system SHALL pass only retrieved tenant context to the LLM for answer generation.

#### Scenario: No matching content
- GIVEN a query with no relevant tenant chunks
- WHEN the agent responds
- THEN it states it does not have that information rather than inventing an answer
""",
design="""\
## Approach
- `retrieve()` requires `tenant_id` (contract-enforced). Backend behind the `rag_backend` interface
  (pgvector implementation now; Vertex in MVP 2).

## Hot-path sequence note
Caller turn → STT text → retrieve(tenant_id, query) → context → LLM. Retrieval latency is metered as
its own segment and must fit the sub-1.5s end-to-end turn budget.
""",
tasks="""\
## 1. Interface & implementation
- [ ] 1.1 retrieve(tenant_id, query) interface + pgvector impl
- [ ] 1.2 top-k tuning + metadata return

## 2. Quality & latency
- [ ] 2.1 Latency instrumentation (retrieval portion of turn budget)
- [ ] 2.2 No-match → graceful "I don't have that" path
- [ ] 2.3 Isolation test: cross-tenant retrieval impossibility
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-audio-backend-interface",
capability="audio-backend",
proposal="""\
## Why
Building the abstraction now (even with one backend) is what prevents forked codebases when Gemini
(MVP 2) and NVIDIA self-host (MVP 3) arrive. "Swap the engine, not the car."

## What Changes
Define the `audio_backend` interface (session lifecycle + mandatory usage callback) and the
per-tenant flag resolved by the Tenant Config Router at session setup.

## User-visible impact
None directly; enables MVP 2/3 backends without platform rewrites.

## Rollback
Single backend remains; interface is internal.
""",
spec="""\
## ADDED Requirements

### Requirement: Stable audio-backend contract
The system SHALL define an audio-runtime interface (start session, stream audio in, stream audio
out, end session, report usage) that any backend implements without changes to the shared platform.

#### Scenario: Backend resolved at session setup
- GIVEN a tenant with audio_backend = "cascaded"
- WHEN a call session starts
- THEN the router resolves the backend once at setup (not per turn)
- AND all turns in the session use that backend

### Requirement: Usage reporting from every backend
The system SHALL require each backend to emit per-session usage (audio seconds, tokens where
applicable) to the metering plane.

#### Scenario: Usage emitted regardless of backend
- GIVEN any registered audio backend
- WHEN a session ends
- THEN a usage record is emitted with tenant_id, backend, and consumption metrics
""",
design="""\
## Approach
- Interface contract lives in the shared platform; `cascaded` is the first implementation.
- Router reads the flag from the tenant config store at session start (never per turn — latency).
- The usage callback is **mandatory in the contract**: a backend that does not emit usage fails the
  conformance suite and cannot register.

## Conformance
Ship a conformance test suite any backend must pass (lifecycle, usage emission, error behavior).
This is the gate MVP 2/3 backends will be held to.
""",
tasks="""\
## 1. Contract
- [ ] 1.1 Define audio_backend interface (lifecycle + usage callback)
- [ ] 1.2 Conformance test suite any backend must pass

## 2. Routing
- [ ] 2.1 Router resolves backend at session setup from config store
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-audio-cascaded",
capability="audio-cascaded",
proposal="""\
## Why
The MVP-default voice runtime; fastest to ship, zero GPU ops.

## What Changes
Implement the cascaded pipeline behind the audio interface: LiveKit + Deepgram STT + Claude
(Haiku/Sonnet cost routing) + Cartesia TTS, with VAD turn-taking and barge-in.

## User-visible impact
Callers have a real-time, grounded spoken conversation with the tenant's agent.

## Rollback
Disable inbound sessions per tenant via flag.
""",
spec="""\
## ADDED Requirements

### Requirement: Real-time cascaded voice turn
The system SHALL transcribe caller speech, retrieve context, generate a grounded response, and
synthesize speech within a target end-to-end turn latency of 1.5s (p50).

#### Scenario: Caller asks a grounded question
- GIVEN a configured tenant agent
- WHEN a caller asks a question covered by tenant docs
- THEN the agent responds with a grounded spoken answer within the latency target

### Requirement: Cost-routed inference
The system SHALL route trivial turns to a cheaper model (Haiku) and substantive turns to the anchor
model (Sonnet).

#### Scenario: Trivial turn routed cheaply
- GIVEN a greeting or acknowledgement turn
- WHEN the router classifies it as trivial
- THEN the cheaper model handles it and the choice is recorded in metering

### Requirement: Barge-in / turn-taking
The system SHALL support caller interruption (barge-in) and voice-activity-based turn-taking.

#### Scenario: Caller interrupts the agent
- GIVEN the agent is speaking
- WHEN the caller starts speaking
- THEN the agent stops and listens
""",
design="""\
## Approach
- LiveKit Agents (Python) orchestrates STT/LLM/TTS. Each vendor sits behind an internal interface
  (swappable: no business logic may depend on a vendor SDK surface).
- LLM router classifies turn complexity (target mix ~Haiku 30% / Sonnet 70%).
- Conversation/turn state held in the session runtime; VAD-driven turn-taking and barge-in owned here.

## Hot-path sequence note
audio in → VAD/turn detect → STT → (retrieve) → LLM (routed) → TTS → audio out. Each segment is
instrumented separately for the latency budget and metering.
""",
tasks="""\
## 1. Pipeline
- [ ] 1.1 LiveKit Agents session wiring
- [ ] 1.2 Deepgram STT behind STT interface
- [ ] 1.3 LLM router (Haiku/Sonnet) behind LLM interface
- [ ] 1.4 Cartesia TTS behind TTS interface

## 2. Conversation behavior
- [ ] 2.1 Barge-in + VAD turn-taking

## 3. Telemetry
- [ ] 3.1 Per-turn latency + model-choice telemetry (feeds metering + observability)
- [ ] 3.2 Pass audio-backend conformance suite
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-channel-ingress",
capability="channel-ingress",
proposal="""\
## Why
Web/mobile use WebRTC, but WhatsApp and IVR-replacement (SIP) do not. Building the adapter seam now
means later channels don't require runtime surgery.

## What Changes
Add a channel-ingress layer presenting a uniform session to the audio runtime; implement WebRTC now;
stub SIP + WhatsApp adapters with explicit not-enabled behavior.

## User-visible impact
Widget works on web/mobile; future channels slot in cleanly.

## Rollback
Only WebRTC enabled.
""",
spec="""\
## ADDED Requirements

### Requirement: Channel-adapter seam
The system SHALL place a channel-ingress layer in front of the transport so that WebRTC, SIP, and
WhatsApp adapters present a uniform session to the audio runtime.

#### Scenario: WebRTC call enters via adapter
- GIVEN a caller on the web widget
- WHEN the call connects
- THEN a WebRTC adapter normalizes it into a uniform session for the audio runtime

#### Scenario: Unsupported channel fails cleanly
- GIVEN a channel with no implemented adapter (e.g., SIP in MVP 1)
- WHEN a connection is attempted
- THEN it is rejected with a clear "channel not enabled" response (no silent failure)
""",
design="""\
## Approach
- Uniform session abstraction; WebRTC adapter over LiveKit.
- SIP/WhatsApp adapters are interface stubs documented for MVP 2/3 — they exist so the seam is real,
  and they answer connections with an explicit not-enabled response.
""",
tasks="""\
## 1. Seam
- [ ] 1.1 Uniform session abstraction
- [ ] 1.2 WebRTC adapter (LiveKit)

## 2. Stubs
- [ ] 2.1 SIP + WhatsApp adapter interface stubs (explicit not-enabled response)
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-voice-widget",
capability="voice-widget",
proposal="""\
## Why
The embeddable widget is the product's "catch" — same script, every site, zero cross-tenant leakage.

## What Changes
Ship `widget.js` loaded via one `<script>` tag with a `data-tenant` attribute; CDN-served, versioned.

## User-visible impact
A tenant pastes one snippet and the branded voice agent appears on their site or mobile-app WebView.

## Rollback
Widget CDN version pinned; rollback to prior bundle.
""",
spec="""\
## ADDED Requirements

### Requirement: Single-snippet embed
The system SHALL provide one `widget.js` that renders a tenant's branded voice widget based solely
on the `data-tenant` attribute, with no cross-tenant data leakage.

#### Scenario: Two tenants, same script
- GIVEN AcmePay and TelcoOne each embed widget.js with their own data-tenant
- WHEN each site loads
- THEN each shows its own branding/agent and connects only to its own tenant session

### Requirement: Mobile WebView support
The system SHALL function inside a mobile-app WebView, not only desktop browsers.

#### Scenario: Widget in a WebView
- GIVEN a mobile app embedding the widget in a WebView
- WHEN a user starts a voice session
- THEN the session functions equivalently to desktop web
""",
design="""\
## Approach
- Framework-free TypeScript bundle; reads `data-tenant`; establishes a session via the channel-ingress
  layer (WebRTC adapter). Branding/persona fetched per tenant. CDN-served, versioned, pinned.
""",
tasks="""\
## 1. Bundle
- [ ] 1.1 widget.js bundle (data-tenant driven)
- [ ] 1.2 Session bootstrap via channel-ingress

## 2. Branding & platforms
- [ ] 2.1 Per-tenant branding/persona fetch
- [ ] 2.2 Mobile WebView validation
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-agent-configuration",
capability="agent-configuration",
proposal="""\
## Why
Tenants must configure persona, greeting, escalation rules, and hours without code.

## What Changes
Portal configuration surface + persisted agent config per tenant, consumed by the runtime at session setup.

## User-visible impact
Self-serve agent setup in the portal.

## Rollback
Defaults applied if config absent.
""",
spec="""\
## ADDED Requirements

### Requirement: No-code agent configuration
The system SHALL let a tenant set persona (name/voice/tone), greeting, business hours, escalation
rules, and human-fallback behavior via the portal.

#### Scenario: Tenant sets business hours
- GIVEN a tenant admin in the portal
- WHEN they set business hours and an out-of-hours message
- THEN calls outside hours use the configured behavior
""",
design="""\
## Approach
- Agent config persisted per tenant; consumed by the audio runtime at session setup (not mid-call).
- Persona/voice selection constrained to voices available on the tenant's configured audio backend.
""",
tasks="""\
## 1. Config
- [ ] 1.1 Agent config schema + portal UI
- [ ] 1.2 Persona/voice/greeting/hours/escalation fields

## 2. Runtime
- [ ] 2.1 Runtime consumption at session setup
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-crm-escalation",
capability="crm-escalation",
proposal="""\
## Why
"Fallback to human" and CRM ticketing are sold on the deck; they are core product, not add-ons.

## What Changes
Add a human-escalation path with context handoff + CRM connectors (Zendesk/Freshdesk first) via webhook.

## User-visible impact
Unresolved calls escalate to a human with full context; tickets are created automatically.

## Rollback
Escalation disabled → agent-only mode per tenant.
""",
spec="""\
## ADDED Requirements

### Requirement: Human escalation path
The system SHALL escalate a call to a human per the tenant's escalation rules and pass conversation
context to the destination.

#### Scenario: Agent cannot resolve
- GIVEN an escalation rule "transfer on explicit request or low confidence"
- WHEN the trigger occurs
- THEN the call is handed off with the transcript and retrieved context attached

### Requirement: CRM ticket creation
The system SHALL create a ticket in the tenant's connected CRM on escalation via webhook.

#### Scenario: Escalation creates a ticket
- GIVEN a connected Zendesk integration
- WHEN an escalation fires
- THEN a ticket is created with the conversation summary and metadata
""",
design="""\
## Approach
- Escalation hangs off the LLM/runtime layer (explicit-request + low-confidence triggers in MVP 1;
  sentiment-aware triggers arrive in Phase 4 — leave the trigger interface open).
- CRM connectors behind an interface; Zendesk/Freshdesk first, HubSpot/custom next.
- Context bundle = transcript + retrieved chunks + metadata. Webhook delivery with retry.
""",
tasks="""\
## 1. Escalation
- [ ] 1.1 Escalation trigger rules + handoff path
- [ ] 1.2 Context bundle assembly

## 2. CRM
- [ ] 2.1 CRM connector interface + Zendesk/Freshdesk impls
- [ ] 2.2 Webhook delivery + retry
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-usage-metering",
capability="usage-metering",
proposal="""\
## Why
A usage-priced business must meter minutes/tokens/STT-TTS/retrieval per tenant in real time to
enforce caps, bill overage, and surface margin leakage immediately. Margin-critical; expensive to retrofit.

## What Changes
Add a metering + telemetry plane that taps every backend's mandatory usage callback and feeds billing
plus an internal margin dashboard.

## User-visible impact
Accurate usage in the portal; overage billing possible; internal real-time margin view.

## Rollback
Metering is read-only telemetry first; billing consumption gated behind a flag.
""",
spec="""\
## ADDED Requirements

### Requirement: Per-tenant real-time metering
The system SHALL meter, per tenant and per session, voice minutes, STT/TTS seconds, LLM tokens (by
model), and retrieval calls, available in near real time.

#### Scenario: A call is fully metered
- GIVEN a completed call on any backend
- WHEN the session ends
- THEN a metering record captures minutes, STT/TTS seconds, tokens by model, and retrieval count
- AND the tenant's running usage updates within minutes

### Requirement: Cap enforcement
The system SHALL enforce tier minute/conversation caps and flag overage.

#### Scenario: Tenant hits cap
- GIVEN a Starter tenant at its monthly cap
- WHEN another call begins
- THEN the system applies the tenant's overage policy (block or bill-overage) per configuration
""",
design="""\
## Approach
- High-throughput collector service (Go) ingesting usage events from every backend's mandatory
  usage callback. Durable store; near-real-time aggregation per tenant.
- Feeds (a) billing and (b) an internal **margin dashboard** (revenue vs vendor cost per tenant).
- Metering accuracy is a correctness requirement: reconciliation tests against vendor invoices.
""",
tasks="""\
## 1. Pipeline
- [ ] 1.1 Usage event schema (tenant, session, backend, metrics)
- [ ] 1.2 Collector service (Go) + durable store
- [ ] 1.3 Backend usage-callback integration (cascaded first)

## 2. Enforcement & visibility
- [ ] 2.1 Cap evaluation + overage policy hook
- [ ] 2.2 Margin dashboard (revenue vs vendor cost per tenant)
- [ ] 2.3 Reconciliation tests vs vendor invoices
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-billing-subscription",
capability="billing-subscription",
proposal="""\
## Why
Recurring subscription + metered overage is the business model.

## What Changes
Stripe subscriptions (3 tiers, operative enterprise pricing), entitlement enforcement, overage billing
fed by the metering plane.

## User-visible impact
Tenants subscribe to a tier and are billed monthly, with overage where configured.

## Rollback
Billing in test mode; enforcement flag-gated.
""",
spec="""\
## ADDED Requirements

### Requirement: Tiered subscription
The system SHALL support Starter/Growth/Scale subscriptions with the operative enterprise pricing,
enforcing tier entitlements.

#### Scenario: Tier gates features
- GIVEN a Starter subscription
- WHEN the tenant attempts a Growth-only feature
- THEN it is gated with an upgrade prompt

### Requirement: Metered overage billing
The system SHALL bill overage beyond tier caps using metering data.

#### Scenario: Overage billed
- GIVEN a tenant exceeding its cap with bill-overage policy
- WHEN the billing period closes
- THEN overage is charged per the published overage rate
""",
design="""\
## Approach
- Stripe subscriptions + metered usage records pushed from the metering plane.
- Entitlements map to tier; enforcement middleware in the control plane.
- Pricing = enterprise card from project.md (Starter $2–5k / Growth $10–20k / Scale $30–60k).
  The discarded $99/$499 placeholder pricing MUST NOT be implemented.
""",
tasks="""\
## 1. Subscription
- [ ] 1.1 Stripe subscription setup (3 tiers)
- [ ] 1.2 Entitlement map + enforcement middleware

## 2. Overage & portal
- [ ] 2.1 Overage push from metering → Stripe
- [ ] 2.2 Billing portal views
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-observability",
capability="observability",
proposal="""\
## Why
Voice is real-time; you cannot operate, debug, or sell SLAs to enterprises without telemetry.

## What Changes
Metrics/traces/logs across call segments + per-tenant operational dashboards + SLO alerting.

## User-visible impact
Internal; underpins SLA claims and incident response.

## Rollback
N/A (additive).
""",
spec="""\
## ADDED Requirements

### Requirement: Live-call telemetry
The system SHALL emit latency, error, and quality metrics per call segment (STT/LLM/TTS/retrieval)
tagged by tenant and backend.

#### Scenario: Latency regression is visible
- GIVEN telemetry is collected
- WHEN turn latency exceeds target
- THEN it is visible on dashboards and alertable

### Requirement: Per-tenant operational view
The system SHALL provide per-tenant dashboards (volume, deflection, errors, usage).

#### Scenario: Tenant operations review
- GIVEN an operator reviewing a tenant
- WHEN they open the tenant dashboard
- THEN volume, deflection, error, and usage trends are visible
""",
design="""\
## Approach
- Metrics/traces/logs pipeline; dashboards per tenant + global. Alerts on latency/error SLOs.
- Segment tagging matches the metering event schema so cost and performance correlate per tenant.
""",
tasks="""\
## 1. Instrumentation
- [ ] 1.1 Instrument call segments (STT/LLM/TTS/retrieval)
- [ ] 1.2 Metrics/traces/logs pipeline

## 2. Visibility
- [ ] 2.1 Per-tenant + global dashboards
- [ ] 2.2 SLO alerts
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-tenant-config-store",
capability="tenant-config-store",
proposal="""\
## Why
The Tenant Config Router needs a control-plane source of truth for per-tenant flags (`tier`,
`language`, `audio_backend`, `rag_backend`, entitlements).

## What Changes
Add a tenant config store with a hot-path read API, consumed by the router at session setup.

## User-visible impact
Internal; enables per-tenant backend routing.

## Rollback
Explicit safe defaults applied if config missing.
""",
spec="""\
## ADDED Requirements

### Requirement: Authoritative tenant config
The system SHALL store per-tenant flags and entitlements and expose them to the router at session setup.

#### Scenario: Router reads config at setup
- GIVEN a tenant config with audio_backend and rag_backend set
- WHEN a session starts
- THEN the router reads the flags once and selects backends accordingly

#### Scenario: Config change applies on next session
- GIVEN a config change made mid-call
- WHEN the current session continues
- THEN the change takes effect on the next session, not mid-call
""",
design="""\
## Approach
- Config store in the control plane; cached for hot-path reads; changes take effect on next session.
- Defaults are explicit and safe (cascaded audio, pgvector RAG).
""",
tasks="""\
## 1. Store
- [ ] 1.1 Config schema (flags + entitlements)
- [ ] 1.2 Read API + hot-path cache

## 2. Integration
- [ ] 2.1 Router integration at session setup
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-consent-capture",
capability="consent-capture",
proposal="""\
## Why
The Pidgin/Swahili language-pack flywheel needs consented production audio; capture must be governed
from day one (NDPR/POPIA): consent, retention, redaction. Legal + strategic.

## What Changes
Add a consent-governed capture pipeline for training-eligible audio, separate from operational data.

## User-visible impact
Callers/tenants see consent; eligible audio is retained lawfully for language-pack training.

## Rollback
Capture off by default; opt-in per tenant.
""",
spec="""\
## ADDED Requirements

### Requirement: Consent-governed capture
The system SHALL capture audio for training only where consent is recorded, with configurable
retention and PII redaction.

#### Scenario: No consent, no capture
- GIVEN a caller who has not consented
- WHEN the call occurs
- THEN no training-eligible audio is retained

#### Scenario: Consented capture with retention
- GIVEN recorded consent
- WHEN the call occurs
- THEN audio is stored in a governed store with retention + redaction applied and tenant scoping
""",
design="""\
## Approach
- Consent state captured at call start (channel-appropriate mechanism per ingress adapter).
- Governed store separate from operational data; redaction pipeline; retention policy enforced.
- Export interface feeds the MVP 3 language-pack data pipeline.
""",
tasks="""\
## 1. Consent
- [ ] 1.1 Consent capture at session start (per channel)

## 2. Governance
- [ ] 2.1 Governed training-audio store (tenant-scoped)
- [ ] 2.2 Retention policy + PII redaction
- [ ] 2.3 Export interface for language-pack pipeline (MVP 3)
""",
),
# ─────────────────────────────────────────────────────────────────────────────
dict(
id="mvp1-failover-baseline",
capability="failover-resilience",
proposal="""\
## Why
Real-time voice cannot have silent single points of failure; a hung call is worse than a failed one.

## What Changes
Add dependency health checks, circuit breakers, a graceful call-failure path to escalation, and
LiveKit transport-resilience basics. (Backend-to-backend failover arrives in MVP 2 when a second
backend exists.)

## User-visible impact
Fewer dropped calls; graceful degradation instead of dead air.

## Rollback
N/A (additive).
""",
spec="""\
## ADDED Requirements

### Requirement: Graceful degradation on vendor failure
The system SHALL detect a failed STT/LLM/TTS dependency and fail the call gracefully (clear message
+ escalation) rather than hanging.

#### Scenario: TTS provider outage
- GIVEN the TTS provider is unavailable
- WHEN a turn needs synthesis
- THEN the call degrades gracefully (e.g., escalation/offer callback), not a dead-air hang

### Requirement: Transport resilience baseline
The system SHALL document and mitigate the LiveKit single-point-of-failure (health checks,
reconnection, capacity headroom).

#### Scenario: Transient transport drop
- GIVEN a transient LiveKit connection drop
- WHEN the client reconnects within the window
- THEN the session resumes without restarting the conversation
""",
design="""\
## Approach
- Health checks per dependency; circuit breaker + graceful path to escalation/callback.
- LiveKit reconnection + documented capacity headroom; SPOF analysis recorded.
- Leaves the failover-controller seam open for MVP 2's B→A backend failover.
""",
tasks="""\
## 1. Dependency resilience
- [ ] 1.1 Dependency health checks + circuit breakers
- [ ] 1.2 Graceful call-failure path → escalation/callback

## 2. Transport
- [ ] 2.1 LiveKit reconnection + capacity headroom
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
    write(os.path.join(base, "design.md"), DESIGN_HEADER.format(id=ch["id"]) + ch["design"])
    write(os.path.join(base, "tasks.md"), TASKS_HEADER.format(id=ch["id"]) + ch["tasks"])
    count += 4

print(f"Wrote {count} files across {len(CHANGES)} changes under {ROOT}")
