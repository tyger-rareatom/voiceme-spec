# Proposal: mvp1-workflow-engine

## Status
**Phase: MVP 1 — Blocked by:** `mvp1-tenant-provisioning`, `mvp1-tenant-config-store`,
`mvp1-usage-metering`, `mvp1-observability`. **Prerequisite for:** `mvp1-knowledge-gap-loop`,
`mvp2-follow-through`, `mvp2-complaint-cases`, and Phase 4 `outbound-voice`.

## Why
Every call ends answered, escalated, or with "I don't have that information". The last two are dead
ends: `mvp1-failover-baseline` and `mvp2-action-packs` offer callers a callback, and
`mvp1-rag-retrieval` stops at "it states it does not have that information", but no capability owns
what happens next. Buyers measure exactly these outcomes: unanswered enquiries, broken callback
promises, complaint deadlines missed.

The three customer workflows that close these gaps (knowledge gaps, follow-through, complaint cases)
share one shape: an event from a call starts a long-running process with timers, notifications and
escalations that runs for hours or days after the call ends. Building that once, as a platform engine,
avoids three separate half-reliable implementations.

## What Changes
- Add **workflow events** emitted by the session runtime through a transactional outbox (no event lost,
  never blocking the turn).
- Add a **workflow service** that runs versioned workflow templates per tenant, with durable state,
  durable timers, retries and idempotent actions.
- Add **notification adapters** behind one interface: email (send and reply ingestion) and SMS first;
  WhatsApp and outbound voice arrive with later changes.
- Meter every notification; enforce a per-tenant monthly notification cap.
- Alert on overdue workflow steps.

## User-visible impact
Internal platform capability. Tenants see it through the three workflow changes it enables.

## Rollback
Additive. Templates are enabled per tenant by flag; with none enabled, no workflow runs. Outbox rows are
retained until consumed, so the service can be stopped and restarted without loss.

## Out of scope
- Tenant-authored custom workflows or a visual builder (Phase 5 developer platform).
- Outbound voice calls (Phase 4 `outbound-voice` adds an adapter to this engine).
