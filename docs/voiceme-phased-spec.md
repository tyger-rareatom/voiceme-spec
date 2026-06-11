# VoiceMe — Phased Product Specification (OpenSpec-ready)

> **How to read this.** Each phase below contains **changes** (OpenSpec change packages).
> Every change is laid out in the OpenSpec idiom: **proposal → spec delta (requirements with
> Given/When/Then scenarios) → design → tasks**. Capability names map to `openspec/specs/<capability>/`.
>
> **OpenSpec philosophy honoured:** specs are created as needed, not all upfront. **MVP 1 changes are
> fully specified** (build now). **MVP 2–3 are moderately specified** (propose when reached).
> **Phases 4–5 are stubs** (roadmap intent; expand into full changes at the time).
>
> To operationalize: run `openspec init`, drop `project.md` in, then for each change run
> `/opsx:propose <change-id>` and paste the relevant section, or scaffold the folders directly.

---

## Phase index

| Phase | Theme | Window | Status in this doc |
|---|---|---|---|
| **MVP 1** | Standard platform GA | Months 1–5 | Fully specified |
| **MVP 2** | Premium / Scale tier + sovereign | Months 5–9 | Moderately specified |
| **MVP 3** | Africa language moat (NVIDIA path) | Year 1–2 | Moderately specified |
| **Phase 4** | Agentic actions & intelligence | Year 2 | Stub |
| **Phase 5** | Scale & expansion | Year 2+ | Stub |

---
---

# MVP 1 — Standard platform GA

**Goal:** a multi-tenant, billable, observable voice-support platform on the cascaded stack, with
three working tenants (AcmePay, TelcoOne, one paying anchor) live on real traffic.

**Definition of done:** a tenant can self-serve sign up, upload docs, configure an agent, copy an
embed snippet, and take grounded voice calls that are metered, billed, escalatable to a human, and
observable — with backend selection abstracted so MVP 2/3 backends slot in without platform changes.

**MVP 1 deliverables (the phase ships when all are GA):**
1. Tenant provisioning & isolation
2. Knowledge ingestion (continuous-learning RAG pipeline)
3. RAG retrieval (tenant-scoped)
4. Audio-backend interface (abstraction + config flag) — **built now even with one backend**
5. Cascaded audio runtime
6. Channel-ingress abstraction (WebRTC now; SIP/WhatsApp adapters stubbed)
7. Voice widget (`widget.js`)
8. Agent configuration (persona, greeting, escalation rules, hours)
9. CRM integration + human escalation
10. Usage metering & telemetry plane
11. Billing & subscription (Stripe + tier enforcement + overage)
12. Observability & per-tenant dashboards
13. Tenant config store (control plane for flags)
14. Consent capture & data-governance pipeline
15. Failover & resilience (baseline)

---

## Change: `mvp1-tenant-provisioning`
**Capability:** `tenant-provisioning` · **Phase:** MVP 1

### proposal.md
- **Why:** Every other capability depends on a tenant existing and being isolated. This is the root.
- **What changes:** Add sign-up, auth, branded subdomain provisioning, and a tenant-scoped data model.
- **User-visible impact:** A business can create an account and receive an isolated workspace.
- **Rollback:** Feature-flag sign-up closed; existing tenants unaffected (additive schema only).

### specs/tenant-provisioning/spec.md
```
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
```

### design.md
- Control-plane service (FastAPI). Postgres with a `tenants` table and a **tenant-scoped repository
  layer** that requires `tenant_id` on every query; unscoped queries forbidden by lint/review.
- Subdomain provisioning via wildcard DNS + per-tenant routing.
- Auth via OIDC-compatible provider; sessions carry `tenant_id` + role claims.

### tasks.md
```
- [ ] 1.1 Create tenants + users schema with tenant_id FKs
- [ ] 1.2 Implement tenant-scoped repository base class (requires tenant_id)
- [ ] 1.3 Sign-up + email verification flow
- [ ] 1.4 Wildcard-subdomain provisioning + routing
- [ ] 1.5 Role model (admin/member) + authorization middleware
- [ ] 1.6 Cross-tenant access test suite (must prove isolation)
```

---

## Change: `mvp1-knowledge-ingestion`
**Capability:** `knowledge-ingestion` · **Phase:** MVP 1

### proposal.md
- **Why:** The continuous-learning RAG pipeline is the core differentiator ("learns within the hour").
- **What changes:** Add doc upload (PDF/DOCX/MD/URL), chunking, embedding, indexing, and re-index on update.
- **User-visible impact:** A tenant uploads FAQs/how-tos/product docs; the agent reflects them shortly after.
- **Rollback:** Disable ingestion endpoint; existing indexes remain queryable.

### specs/knowledge-ingestion/spec.md
```
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
```

### design.md
- Ingestion worker (async queue). Chunker → embeddings (Voyage for Standard) → pgvector upsert.
- Idempotent re-index keyed by document hash; soft-delete superseded chunks.
- Embedding provider behind an interface (Voyage now; Vertex path in MVP 2).

### tasks.md
```
- [ ] 1.1 Upload endpoint + storage (PDF/DOCX/MD/URL fetchers)
- [ ] 1.2 Chunker with source metadata
- [ ] 1.3 Embedding provider interface + Voyage implementation
- [ ] 1.4 pgvector upsert + tenant scoping
- [ ] 1.5 Re-index on update (hash-keyed, idempotent)
- [ ] 1.6 Ingestion status surfaced in portal
```

---

## Change: `mvp1-rag-retrieval`
**Capability:** `rag-retrieval` · **Phase:** MVP 1

### proposal.md
- **Why:** Grounded answers require tenant-scoped retrieval in the live-call hot path.
- **What changes:** Add a retrieval API that returns top-k chunks for a query, scoped by tenant.
- **User-visible impact:** The agent answers from the tenant's own content only.
- **Rollback:** N/A (additive); retrieval can be bypassed for a tenant via flag for debugging.

### specs/rag-retrieval/spec.md
```
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
```

### design.md
- `retrieve()` requires `tenant_id` (compile-time/contract-enforced). Backend behind `rag_backend`
  interface (pgvector now). Latency budget: retrieval must fit the sub-1.5s end-to-end turn target.

### tasks.md
```
- [ ] 1.1 retrieve(tenant_id, query) interface + pgvector impl
- [ ] 1.2 top-k tuning + metadata return
- [ ] 1.3 Latency instrumentation (retrieval portion of turn budget)
- [ ] 1.4 No-match → graceful "I don't have that" path
```

---

## Change: `mvp1-audio-backend-interface`
**Capability:** `audio-backend` · **Phase:** MVP 1 · **Critical for future phases**

### proposal.md
- **Why:** Building the abstraction now (even with one backend) is what prevents forked codebases later.
- **What changes:** Define the `audio_backend` interface + per-tenant flag resolved at session setup.
- **User-visible impact:** None directly; enables MVP 2/3 backends without platform rewrites.
- **Rollback:** Single backend remains; interface is internal.

### specs/audio-backend/spec.md
```
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
```

### design.md
- Interface contract in shared platform; `cascaded` is the first implementation. Router reads the
  flag from the tenant config store at session start. Usage callback is mandatory in the contract.

### tasks.md
```
- [ ] 1.1 Define audio_backend interface (lifecycle + usage callback)
- [ ] 1.2 Router resolves backend at session setup from config store
- [ ] 1.3 Conformance test any backend must pass
```

---

## Change: `mvp1-audio-cascaded`
**Capability:** `audio-cascaded` · **Phase:** MVP 1

### proposal.md
- **Why:** The MVP-default voice runtime; fastest to ship, no GPU ops.
- **What changes:** Implement cascaded pipeline behind the interface: LiveKit + Deepgram STT +
  Claude (Haiku/Sonnet routing) + Cartesia TTS, with turn-taking/barge-in.
- **User-visible impact:** Callers have a real-time spoken conversation with the agent.
- **Rollback:** Disable inbound sessions per tenant via flag.

### specs/audio-cascaded/spec.md
```
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
```

### design.md
- LiveKit Agents (Python) orchestrates STT/LLM/TTS. Vendors behind internal interfaces (swappable).
- LLM router classifies turn complexity (Haiku 30% / Sonnet 70%). Conversation/turn state held in
  the session runtime; VAD-driven turn-taking and barge-in handling owned here.

### tasks.md
```
- [ ] 1.1 LiveKit Agents session wiring
- [ ] 1.2 Deepgram STT behind STT interface
- [ ] 1.3 LLM router (Haiku/Sonnet) behind LLM interface
- [ ] 1.4 Cartesia TTS behind TTS interface
- [ ] 1.5 Barge-in + VAD turn-taking
- [ ] 1.6 Per-turn latency + model-choice telemetry
```

---

## Change: `mvp1-channel-ingress`
**Capability:** `channel-ingress` · **Phase:** MVP 1

### proposal.md
- **Why:** Web/mobile use WebRTC, but WhatsApp and IVR-replacement (SIP) do not. Build the adapter
  seam now so later channels don't require runtime surgery.
- **What changes:** Add a channel-ingress layer; implement WebRTC now; stub SIP + WhatsApp adapters.
- **User-visible impact:** Widget works on web/mobile; future channels slot in.
- **Rollback:** Only WebRTC enabled.

### specs/channel-ingress/spec.md
```
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
```

### design.md
- Uniform session abstraction; WebRTC adapter over LiveKit. SIP/WhatsApp adapters are interface
  stubs documented for MVP 2/3. Prevents the "all ingress is WebRTC" error.

### tasks.md
```
- [ ] 1.1 Uniform session abstraction
- [ ] 1.2 WebRTC adapter (LiveKit)
- [ ] 1.3 SIP + WhatsApp adapter interface stubs (explicit not-enabled response)
```

---

## Change: `mvp1-voice-widget`
**Capability:** `voice-widget` · **Phase:** MVP 1

### proposal.md
- **Why:** The embeddable widget is the product's "catch" — same script, every site.
- **What changes:** Ship `widget.js` loaded via one `<script>` tag with `data-tenant`.
- **User-visible impact:** A tenant pastes one snippet and the voice agent appears on their site/app.
- **Rollback:** Widget CDN version pinned; rollback to prior bundle.

### specs/voice-widget/spec.md
```
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
```

### design.md
- Framework-free bundle; reads `data-tenant`; establishes a WebRTC session via the channel-ingress
  layer. Branding/persona fetched per tenant. CDN-served, versioned.

### tasks.md
```
- [ ] 1.1 widget.js bundle (data-tenant driven)
- [ ] 1.2 Session bootstrap via channel-ingress
- [ ] 1.3 Per-tenant branding/persona fetch
- [ ] 1.4 Mobile WebView validation
```

---

## Change: `mvp1-agent-configuration`
**Capability:** `agent-configuration` · **Phase:** MVP 1

### proposal.md
- **Why:** Tenants must configure persona, greeting, escalation rules, and hours without code.
- **What changes:** Portal configuration surface + persisted agent config per tenant.
- **User-visible impact:** Self-serve agent setup.
- **Rollback:** Defaults applied if config absent.

### specs/agent-configuration/spec.md
```
## ADDED Requirements

### Requirement: No-code agent configuration
The system SHALL let a tenant set persona (name/voice/tone), greeting, business hours, escalation
rules, and human-fallback behavior via the portal.

#### Scenario: Tenant sets business hours
- GIVEN a tenant admin in the portal
- WHEN they set business hours and an out-of-hours message
- THEN calls outside hours use the configured behavior
```

### design.md
- Agent config persisted per tenant; consumed by the audio runtime at session setup. Persona/voice
  selection constrained to available voices per backend.

### tasks.md
```
- [ ] 1.1 Agent config schema + portal UI
- [ ] 1.2 Persona/voice/greeting/hours/escalation fields
- [ ] 1.3 Runtime consumption at session setup
```

---

## Change: `mvp1-crm-escalation`
**Capability:** `crm-escalation` · **Phase:** MVP 1

### proposal.md
- **Why:** "Fallback to human" and CRM ticketing are sold on the deck; they're core, not optional.
- **What changes:** Add human-escalation path + CRM webhooks (Zendesk/Freshdesk/HubSpot/custom).
- **User-visible impact:** Unresolved calls escalate to a human; tickets are created.
- **Rollback:** Escalation disabled → agent-only mode per tenant.

### specs/crm-escalation/spec.md
```
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
```

### design.md
- Escalation hangs off the LLM/runtime layer. CRM connectors behind an interface (Zendesk/Freshdesk
  first). Context bundle = transcript + retrieved chunks + sentiment placeholder (full sentiment in Phase 4).

### tasks.md
```
- [ ] 1.1 Escalation trigger rules + handoff path
- [ ] 1.2 Context bundle assembly
- [ ] 1.3 CRM connector interface + Zendesk/Freshdesk impls
- [ ] 1.4 Webhook delivery + retry
```

---

## Change: `mvp1-usage-metering`
**Capability:** `usage-metering` · **Phase:** MVP 1 · **Margin-critical**

### proposal.md
- **Why:** A usage-priced business must meter minutes/tokens/STT-TTS/retrieval per tenant in real
  time to enforce caps, bill overage, and see margin leakage immediately.
- **What changes:** Add a metering + telemetry plane that taps every backend and feeds billing.
- **User-visible impact:** Accurate usage in portal; overage billing possible; internal margin dashboard.
- **Rollback:** Metering is read-only telemetry first; billing consumption gated behind a flag.

### specs/usage-metering/spec.md
```
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
```

### design.md
- High-throughput collector (Go) ingesting usage events from every backend's mandatory usage
  callback. Feeds (a) billing and (b) an internal **margin dashboard** (revenue vs vendor cost per
  tenant). Treat metering accuracy as a correctness requirement (reconciliation tests vs vendor bills).

### tasks.md
```
- [ ] 1.1 Usage event schema (tenant, session, backend, metrics)
- [ ] 1.2 Collector service (Go) + durable store
- [ ] 1.3 Backend usage-callback integration (cascaded first)
- [ ] 1.4 Cap evaluation + overage policy hook
- [ ] 1.5 Margin dashboard (revenue vs vendor cost per tenant)
- [ ] 1.6 Reconciliation tests vs vendor invoices
```

---

## Change: `mvp1-billing-subscription`
**Capability:** `billing-subscription` · **Phase:** MVP 1

### proposal.md
- **Why:** Recurring subscription + metered overage is the business model.
- **What changes:** Stripe subscriptions, tier enforcement, overage billing from metering.
- **User-visible impact:** Tenants subscribe to a tier and are billed monthly (+ overage).
- **Rollback:** Billing in test mode; enforcement flag-gated.

### specs/billing-subscription/spec.md
```
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
```

### design.md
- Stripe subscriptions + metered usage records pushed from the metering plane. Entitlements map to
  tier. Pricing = enterprise card from `project.md` (placeholder $99/$499 explicitly excluded).

### tasks.md
```
- [ ] 1.1 Stripe subscription setup (3 tiers)
- [ ] 1.2 Entitlement map + enforcement middleware
- [ ] 1.3 Overage push from metering → Stripe
- [ ] 1.4 Billing portal views
```

---

## Change: `mvp1-observability`
**Capability:** `observability` · **Phase:** MVP 1

### proposal.md
- **Why:** Voice is real-time; you cannot operate or sell to enterprises without telemetry.
- **What changes:** Metrics/traces/logs + per-tenant operational dashboards + alerting.
- **User-visible impact:** Internal; underpins SLA claims.
- **Rollback:** N/A (additive).

### specs/observability/spec.md
```
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
```

### design.md
- Metrics/traces/logs pipeline; dashboards per tenant + global. Alerts on latency/error SLOs.

### tasks.md
```
- [ ] 1.1 Instrument call segments (STT/LLM/TTS/retrieval)
- [ ] 1.2 Metrics/traces/logs pipeline
- [ ] 1.3 Per-tenant + global dashboards
- [ ] 1.4 SLO alerts
```

---

## Change: `mvp1-tenant-config-store`
**Capability:** `tenant-config-store` · **Phase:** MVP 1

### proposal.md
- **Why:** The router needs a control-plane source of truth for per-tenant flags (`tier`, `language`,
  `audio_backend`, `rag_backend`, entitlements).
- **What changes:** Add a tenant config store read at session setup.
- **User-visible impact:** Internal; enables routing.
- **Rollback:** Defaults applied if config missing.

### specs/tenant-config-store/spec.md
```
## ADDED Requirements

### Requirement: Authoritative tenant config
The system SHALL store per-tenant flags and entitlements and expose them to the router at session setup.

#### Scenario: Router reads config at setup
- GIVEN a tenant config with audio_backend and rag_backend set
- WHEN a session starts
- THEN the router reads the flags once and selects backends accordingly
```

### design.md
- Config store in the control plane; cached for hot-path reads; changes take effect on next session
  (not mid-call). Defaults are explicit and safe.

### tasks.md
```
- [ ] 1.1 Config schema (flags + entitlements)
- [ ] 1.2 Read API + hot-path cache
- [ ] 1.3 Router integration at session setup
```

---

## Change: `mvp1-consent-capture`
**Capability:** `consent-capture` · **Phase:** MVP 1 · **Legal + strategic**

### proposal.md
- **Why:** The Pidgin/Swahili language-pack flywheel needs consented production audio; capture must
  be governed from day one (NDPR/POPIA): consent, retention, redaction.
- **What changes:** Add a consent-governed capture pipeline for training-eligible audio.
- **User-visible impact:** Callers/tenants see consent; eligible audio is retained lawfully.
- **Rollback:** Capture off by default; opt-in per tenant.

### specs/consent-capture/spec.md
```
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
```

### design.md
- Consent state captured at call start (channel-appropriate). Governed store separate from
  operational data; redaction pipeline; retention policy enforced. Feeds MVP 3 language-pack data.

### tasks.md
```
- [ ] 1.1 Consent capture at session start (per channel)
- [ ] 1.2 Governed training-audio store (tenant-scoped)
- [ ] 1.3 Retention policy + PII redaction
- [ ] 1.4 Export interface for language-pack pipeline (MVP 3)
```

---

## Change: `mvp1-failover-baseline`
**Capability:** `failover-resilience` · **Phase:** MVP 1

### proposal.md
- **Why:** Real-time voice cannot have silent single points of failure.
- **What changes:** Add health checks, graceful call failure, and transport redundancy basics.
- **User-visible impact:** Fewer dropped calls; graceful degradation.
- **Rollback:** N/A (additive).

### specs/failover-resilience/spec.md
```
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
```

### design.md
- Health checks per dependency; circuit-breaker + graceful path to escalation. Full backend-to-backend
  failover (B→A) lands in MVP 2 once a second backend exists. LiveKit redundancy/headroom documented.

### tasks.md
```
- [ ] 1.1 Dependency health checks + circuit breakers
- [ ] 1.2 Graceful call-failure path → escalation/callback
- [ ] 1.3 LiveKit reconnection + capacity headroom
```

---
---

# MVP 2 — Premium / Scale tier + sovereign

**Goal:** add the Gemini Live premium audio path and the sovereign Scale-tier posture, behind the
interfaces built in MVP 1, with real failover and tier-upgrade migration.

**MVP 2 deliverables:**
1. Gemini Live audio backend (Option B) behind `audio_backend`
2. Backend failover (B→A on Gemini failure)
3. Vertex AI RAG Engine backend (Option for Scale) + tier-upgrade migration (pgvector→Vertex)
4. Sovereign deployment (in-region VPC, BYOK, audit logging, NDPR/POPIA/SARB controls)
5. Tenant-isolation hardening (dedicated VPC/GPU for sovereign; noisy-neighbour controls)
6. Scale-tier trial gating (real-traffic trial before pricing commitment)

### Change: `mvp2-audio-gemini` (capability `audio-gemini`)
- **proposal:** Add Gemini Live native audio behind the audio interface for covered-language, latency-
  sensitive tenants. **Rollback:** route affected tenants back to cascaded.
- **Key requirements (GWT):**
  - *Requirement: Gemini backend conforms to interface* — GIVEN a tenant flagged `audio_backend=gemini`, WHEN a session starts, THEN Gemini Live serves it and emits usage to metering.
  - *Requirement: Covered-language guard* — GIVEN a tenant language unsupported by Gemini native audio, WHEN configured, THEN the system warns and prevents selection (route to cascaded/NVIDIA).
- **design:** Implement behind `audio_backend`; reuse turn-taking abstraction; note per-turn context
  re-billing (cost-neutral on long calls — value is latency/residency, not cost).
- **tasks:** [ ] Gemini backend impl · [ ] covered-language guard · [ ] usage callback · [ ] latency benchmark vs cascaded.

### Change: `mvp2-backend-failover` (capability `failover-resilience`, MODIFIED)
- **proposal:** Add B→A live failover now that a second backend exists.
- **Key requirements (GWT):** *Requirement: Audio backend failover* — GIVEN `gemini` fails mid-session, WHEN detected, THEN the session fails over to cascaded with minimal disruption and the event is recorded.
- **tasks:** [ ] failover controller · [ ] mid-session switch handling · [ ] failover telemetry.

### Change: `mvp2-rag-vertex` (capability `rag-backend`, MODIFIED + `rag-migration`)
- **proposal:** Add Vertex AI RAG Engine for Scale; migrate a tenant's content on Growth→Scale upgrade.
- **Key requirements (GWT):**
  - *Requirement: Vertex backend behind rag_backend* — GIVEN `rag_backend=vertex`, WHEN retrieval runs, THEN Vertex serves tenant-scoped results.
  - *Requirement: Tier-upgrade migration* — GIVEN a Growth tenant upgrading to Scale, WHEN upgrade completes, THEN content re-indexes from pgvector to Vertex without answer-quality regression.
- **design:** Confirm Vertex RAG Engine availability in target region; migration job idempotent; verify
  fixed node-hour cost only assigned at Scale volume.
- **tasks:** [ ] Vertex backend impl · [ ] migration job · [ ] parity eval pgvector↔Vertex · [ ] region availability check.

### Change: `mvp2-sovereign-deployment` (capability `sovereign-deployment`)
- **proposal:** In-region VPC deployment with BYOK encryption and audit logging for regulated tenants.
- **Key requirements (GWT):**
  - *Requirement: Data residency* — GIVEN a sovereign tenant, WHEN data is processed/stored, THEN it remains in the contracted region.
  - *Requirement: Audit logging* — GIVEN regulated operation, WHEN actions occur, THEN an immutable audit trail is recorded.
  - *Requirement: BYOK* — GIVEN a tenant key, WHEN data is encrypted, THEN the tenant's key is used.
- **tasks:** [ ] in-region VPC topology · [ ] BYOK · [ ] audit log · [ ] NDPR/POPIA/SARB control mapping.

### Change: `mvp2-isolation-hardening` (capability `tenant-isolation`, MODIFIED)
- **proposal:** Dedicated VPC/compute for sovereign tenants; enforce + prove isolation on shared infra.
- **Key requirements (GWT):** *Requirement: Dedicated isolation tier* — GIVEN a sovereign tenant, WHEN provisioned, THEN it runs on dedicated VPC/compute with no shared data plane.
- **tasks:** [ ] dedicated-tenant provisioning mode · [ ] isolation enforcement tests · [ ] noisy-neighbour controls.

### Change: `mvp2-scale-trial-gating` (capability `scale-trial`)
- **proposal:** Gate Scale-tier pricing commitments behind a real-traffic trial.
- **Key requirements (GWT):** *Requirement: Trial before commit* — GIVEN a prospective Scale tenant, WHEN evaluating, THEN a measured real-traffic trial precedes pricing commitment.
- **tasks:** [ ] trial mode · [ ] trial metrics report (latency/cost/quality) · [ ] commit gate.

---
---

# MVP 3 — Africa language moat (NVIDIA path)

**Goal:** own the language layer — self-hosted NVIDIA Riva backend plus fine-tuned Pidgin (then
Swahili) packs — and stand up the GPU operations and the spike-gated Nemotron LLM slot.

**MVP 3 deliverables:**
1. NVIDIA Riva self-host audio backend (Option C) behind `audio_backend`
2. Nigerian Pidgin language pack (data → ASR fine-tune → custom TTS voice → eval)
3. Swahili language pack (East Africa)
4. GPU ops (NIM deployment, autoscaling, MLOps, self-host inflection routing)
5. Nemotron LLM slot + tool-calling spike gate

### Change: `mvp3-audio-nvidia` (capability `audio-nvidia`)
- **proposal:** Self-hosted Riva (Parakeet/Canary ASR + Magpie TTS) behind the audio interface, with
  a swappable LLM slot (Claude default ⇄ Nemotron for fully in-VPC).
- **Key requirements (GWT):**
  - *Requirement: NVIDIA backend conforms* — GIVEN `audio_backend=nvidia`, WHEN a session runs, THEN Riva serves ASR/TTS and emits usage.
  - *Requirement: Volume-gated routing* — GIVEN a low-volume (e.g., Starter) tenant, WHEN backend is chosen, THEN NVIDIA self-host is NOT selected (GPU fixed cost), per the inflection rule.
- **tasks:** [ ] NIM deploy Parakeet/Canary + Magpie · [ ] backend impl + usage · [ ] LLM-slot abstraction (Claude/Nemotron) · [ ] volume-gate routing.

### Change: `mvp3-pidgin-pack` (capability `language-pack-pidgin`) — **critical path is data, not code**
- **proposal:** Build the Nigerian Pidgin pack: consented data → ASR fine-tune → custom Pidgin TTS
  voice → eval harness. **Note:** ship "Pidgin v1" (prompt-steered on cascaded) earlier; "v2" (fine-tuned, owned) here.
- **Key requirements (GWT):**
  - *Requirement: Transcription style guide locked* — GIVEN no standard Pidgin orthography, WHEN labelling begins, THEN a locked style guide governs transcripts.
  - *Requirement: ASR quality bar* — GIVEN the fine-tuned ASR, WHEN evaluated on held-out support calls, THEN WER meets the agreed target vs baseline.
  - *Requirement: Branded Pidgin voice* — GIVEN Magpie voice-clone, WHEN the agent speaks, THEN it uses an approved Nigerian Pidgin voice.
- **design:** Data sources = consented production audio (from MVP 1 consent-capture) + commissioned
  collection + public corpora; ~100–300 hrs labelled; fine-tune Parakeet/Canary; Magpie zero-shot/flow voice.
- **tasks:** [ ] style guide · [ ] data acquisition (commission + harvest) · [ ] ASR fine-tune · [ ] TTS voice · [ ] eval harness on real intents · [ ] route Pidgin tenants → NVIDIA backend.

### Change: `mvp3-swahili-pack` (capability `language-pack-swahili`)
- **proposal:** Replicate the Pidgin workstream for Swahili (East Africa expansion).
- **tasks:** [ ] data · [ ] ASR fine-tune · [ ] TTS voice · [ ] eval · [ ] regional routing.

### Change: `mvp3-gpu-ops` (capability `gpu-ops`)
- **proposal:** Operate self-hosted NIM at production quality: deployment, autoscaling, MLOps, cost
  controls, and the self-host inflection routing.
- **Key requirements (GWT):** *Requirement: Concurrency-aware autoscale* — GIVEN concurrent call load, WHEN capacity nears limits, THEN GPU capacity autoscales within SLO. *Requirement: Inflection routing* — GIVEN per-tenant volume, WHEN above the self-host inflection, THEN eligible tenants route to self-host.
- **tasks:** [ ] NIM deploy/orchestration · [ ] autoscaling on concurrency · [ ] MLOps (model versions/rollback) · [ ] GPU cost telemetry → margin dashboard.

### Change: `mvp3-nemotron-spike` (capability `nemotron-llm`) — **spike-gated**
- **proposal:** De-risk Nemotron tool-calling reliability before any sovereign agentic commitment.
- **Key requirements (GWT):**
  - *Requirement: Tool-call reliability gate* — GIVEN the Nemotron LLM slot, WHEN evaluated on a fixed 50-scenario tool-calling set, THEN tool-selection accuracy is within 5 pts of Claude AND argument JSON-parse validity ≥ 98% AND no-tool discipline ≥ 95% AND latency within budget — else Nemotron is not greenlit for sovereign actions.
- **design:** Serve Nemotron (NIM, detailed-thinking-off) with explicit tool-call parser + chat
  template; eval set drawn from real consented intents; Claude as baseline; 1 engineer / 1 week.
- **tasks:** [ ] serving config (parser/template/thinking-off) · [ ] 50-scenario eval set · [ ] run vs Claude baseline · [ ] decision gate recorded.

---
---

# Phase 4 — Agentic actions & intelligence (stub)

**Goal:** move from "answers" to "actions," plus conversation intelligence and proactive outbound.
Expand into full OpenSpec changes when reached.

**Deliverables (propose later):**
1. **Agentic tool use** (`agentic-actions`) — function calling for order status, password reset,
   refund, booking. Managed tiers on Claude; sovereign on Nemotron **only if the MVP 3 spike passed**.
   Requirements must include confirmation steps, audit trails, and scope limits per action.
2. **Conversation intelligence** (`conversation-intelligence`) — analytics dashboard, sentiment-aware
   escalation, topic clustering, weekly trend reports. (Completes the sentiment placeholder from MVP 1.)
3. **Outbound campaigns** (`outbound-voice`) — proactive calls (reminders, confirmations, retention).
   **Compliance-gated**: opt-in/opt-out, do-not-call, time-of-day, POPIA/Kenya DPA. Not before consent + controls.
4. **Context-rich live-agent handoff** (`agent-handoff`) — full transcript + state + sentiment to the human.

---

# Phase 5 — Scale & expansion (stub)

**Goal:** durability, margin, and reach. Expand into full changes when reached.

**Deliverables (propose later):**
1. **Self-hosted LLM volume migration** (`self-hosted-llm`) — Gemma/Nemotron for sustained high-volume
   tenants above the inflection point; protects margin.
2. **Vertical knowledge templates** (`vertical-templates`) — pre-built RAG packs (fintech/telco/insurance/utility)
   to cut onboarding to minutes.
3. **Compliance certifications as product** (`compliance-certifications`) — ISO 27001, SOC 2, PCI-DSS;
   each unlocks a regulated buyer; package as "Scale Sovereign + Compliance Pack."
4. **Integration marketplace** (`integration-marketplace`) — third-party connectors; network effects.
5. **Multi-region expansion** (`multi-region`) — East/other Africa; region-aware routing + residency.
6. **Developer platform** (`developer-platform`) — API access, webhooks, custom skills; expands TAM.

---
---

## Appendix A — Cross-cutting requirements (apply to every phase)

- **Latency:** end-to-end turn p50 ≤ 1.5s (target sub-1s long-term); backend resolution at session setup.
- **Isolation:** `tenant_id` scoping enforced on every data path; provable by test.
- **Metering:** every backend emits usage; no un-metered consumption path may ship.
- **Failover:** no silent single point of failure on the live-call path.
- **Consent & residency:** capture/storage honor consent + regional residency rules.
- **Vendor swappability:** no business logic hard-depends on a single vendor SDK.
- **Cost routing:** trivial→cheap model, substantive→anchor model, recorded in metering.

## Appendix B — Sequencing dependencies (build-order guardrails)

- `audio-backend` interface + `tenant-config-store` + `usage-metering` are **prerequisites** for every
  audio backend (MVP 1 must precede MVP 2/3 backends).
- `consent-capture` (MVP 1) is a **prerequisite** for `language-pack-*` data (MVP 3).
- `mvp3-nemotron-spike` is a **gate** for Phase 4 sovereign `agentic-actions`.
- `mvp2-backend-failover` requires a second backend to exist (so it follows `mvp2-audio-gemini`).
- Scale-tier pricing commitments require `mvp2-scale-trial-gating` to have run.
