# Proposal: mvp2-compliance-evidence

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-consent-capture`, `mvp1-usage-metering`, `mvp1-observability`,
`mvp1-rag-retrieval`. Sovereign-tenant parts are **blocked by** `mvp2-sovereign-deployment` (they reuse
its append-only audit log). **Extends** `mvp2-sovereign-deployment`'s one-off control-mapping document
into a continuously generated product feature. **Market-leadership capability 3 of 3.**

## Why
In a bank or telco, the customer-experience team is the buyer, but the risk and compliance committee is
the blocker. They ask four questions: where did each call's data go, can every answer be traced to an
approved source, was consent captured, and can we produce evidence for the regulator on demand.

Residency is per country, not per continent: Nigerian data processed in South Africa is still a
cross-border transfer under Nigerian law. VoiceMe targets several African countries, so it needs
per-country rules as data, not code. A platform that arrives with regulator-ready evidence shortens
procurement, and each country profile adds to the moat.

## What Changes
- Add a **jurisdiction profile** per tenant (one or more countries): AI-disclosure wording, consent
  rules per channel, retention periods, cross-border transfer rules, complaint-reporting periods.
  Profiles are versioned data, reviewed by counsel; the first profiles are Nigeria, South Africa and
  Kenya.
- Add an **answer provenance record** for every agent turn: retrieved chunk IDs and document versions,
  tool results used, and the model that answered.
- Add a **cross-border transfer register**, generated from metering events (every usage event already
  names its vendor; this change adds the processing region).
- Add a tenant-scoped **append-only evidence store** for standard tenants; sovereign tenants use the
  `mvp2-sovereign-deployment` audit log.
- Add **evidence reports** (on demand and scheduled): consent records, escalation and complaint handling
  times, transfer register, retention deletions, data-subject request log, provenance samples. Export as
  CSV and PDF (portable document format).
- Add a **data-subject request workflow**: a caller's access or deletion request is logged, routed to
  the tenant, and its completion recorded.

## User-visible impact
- Tenants pick their jurisdiction profile in the portal; disclosures and consent prompts follow it.
- Compliance users can export evidence reports without engineering help.
- Every answer in a transcript links to the source document version it used.

## Rollback
Additive. Provenance and transfer-register recording are on by default and can be paused per tenant by
flag; reports are read-only. Disabling a jurisdiction profile reverts to the platform default disclosure.

## Out of scope
- Legal sign-off on profile contents (counsel owns this; the spec only defines the structure).
- Certifications such as ISO 27001 or SOC 2 (Phase 5 `compliance-certifications`).
