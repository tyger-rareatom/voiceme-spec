# AGENTS.md — VoiceMe (for AI coding assistants)

You are working on **VoiceMe**, a multi-tenant AI voice-agent platform. Before doing anything,
read `openspec/project.md` (the worldview) and the change package you've been asked to implement
under `openspec/changes/<change-id>/`.

## How work happens here (OpenSpec flow)

1. **Never code without a change package.** Work flows proposal → specs → design → tasks → implement.
   If asked to build something with no change package, create the proposal first (`/opsx:propose`).
2. **Implement tasks in order, checking them off** in `tasks.md` as you go (`/opsx:apply`).
3. **When a change ships, archive it** (`/opsx:archive`) so `openspec/specs/` stays the source of truth.
4. **Spec deltas, not rewrites.** When modifying existing behavior, write `MODIFIED Requirements`
   deltas against the current spec — do not regenerate whole specs.

## Phase discipline (do not reorder)

- **MVP 1** is current scope. MVP 2/3 changes must not start until their MVP 1 prerequisites are
  archived: the `audio-backend` interface, `tenant-config-store`, and `usage-metering` precede any
  new audio backend; `consent-capture` precedes any language-pack data work.
- **Gates are gates.** Phase 4 sovereign agentic actions are blocked unless the `mvp3-nemotron-spike`
  pass criteria are met and recorded. Scale-tier pricing commitments require the trial-gating change.

## Hard rules (violations are bugs, not style issues)

1. **Tenant isolation by construction.** All data access goes through the tenant-scoped repository
   layer that *requires* `tenant_id`. Direct unscoped queries are forbidden. Every isolation-touching
   PR includes a cross-tenant denial test.
2. **No un-metered consumption.** Any code path that consumes STT/TTS/LLM/retrieval must emit usage
   to the metering plane. A backend that doesn't implement the usage callback fails conformance and
   cannot register.
3. **Backends are plugins.** Implement against the `audio_backend` / `rag_backend` interfaces. Never
   add backend-specific branches to the shared platform. The router resolves backends **once at
   session setup**, never per turn.
4. **Wrap every vendor.** Business logic never imports a vendor SDK directly (Deepgram, Cartesia,
   Anthropic, Google, Stripe, LiveKit) — always through the internal interface so vendors stay swappable.
5. **Live-call path changes carry a latency note.** State the expected impact on the ≤1.5s p50 turn
   budget and instrument the segment.
6. **Fail loudly, degrade gracefully.** No silent failures on the call path; dependency failure routes
   to the graceful-degradation/escalation path. No dead air, no hangs.
7. **Consent before capture.** Training-eligible audio is only retained where consent is recorded;
   respect retention + redaction. This is law (NDPR/POPIA), not preference.
8. **Pricing guardrail.** Implement only the enterprise pricing card from `project.md`. If you find
   $99/$499 anywhere, that's a bug — flag it.

## Conventions

- **Languages:** Python 3.12 (voice/agent services, FastAPI control plane) · Go 1.22+ (metering
  collector, media edge, high-throughput telemetry) · TypeScript (portal, widget).
- **Style:** type hints everywhere (Python: mypy-clean; TS: strict). Small modules, explicit
  interfaces, dependency injection over globals.
- **Tests:** every requirement's Given/When/Then scenarios map to tests. Isolation and metering get
  negative-case tests. Conformance suite for any new backend.
- **Migrations:** additive-first; destructive migrations need an explicit rollback note in the design.
- **Secrets/config:** never hardcode; per-environment config; tenant flags live in the tenant config
  store, not in code.
- **Commits/PRs:** reference the change id (e.g. `mvp1-usage-metering: 1.2 collector service`).

## When uncertain

- The spec wins over the conversation; `project.md` wins over assumptions; if a requirement is
  ambiguous, propose a spec clarification rather than guessing in code.
- If a task can't be completed atomically, split it in `tasks.md` before coding.
