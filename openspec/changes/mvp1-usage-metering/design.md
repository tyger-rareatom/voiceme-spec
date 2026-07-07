# Design: mvp1-usage-metering

## Approach

- High-throughput collector service (Go) ingesting usage events from every backend's mandatory
  usage callback. Durable store; near-real-time aggregation per tenant.
- Feeds (a) billing and (b) an internal **margin dashboard** (revenue vs vendor cost per tenant).
- Metering accuracy is a correctness requirement: reconciliation tests against vendor invoices.

## Persistence never blocks the audio loop (decision 2026-07-07)

> The turn loop (STT→retrieve→LLM→TTS) performs **no synchronous durability writes**. The only
> sync I/O permitted in-loop is the retrieval read and in-memory breaker/state checks. This rule
> collides with "no un-metered consumption path may ship" the moment async backs up — the
> resolution is per-event-class policy, not a single answer:

| Event class | Block loop? | May drop? | Policy |
| --- | --- | --- | --- |
| Usage/metering | never | never | non-blocking buffer → local durable spool → at-least-once to collector |
| Telemetry/logs/analytics | never | under pressure | bounded buffer, shed oldest, count shed volume |
| Consent training audio | never | fail-closed | governed store unreachable → stop capturing (never capture ungoverned) |
| Escalation transcript/context | never | n/a | session memory during call; persisted after-call |

- **Escape valve = admission control, not blocking or dropping:** if metering durability is
  threatened (spool past threshold, sustained collector outage), the correct degradation is to
  refuse **new** sessions — an un-meterable call is one we'd rather not take — while never
  touching in-flight turns. **MVP-1 scope decision:** admission control is designed and
  flag-gated with an alert-only default (matches the metering-before-enforcement pattern used
  for billing); full block-new-sessions enforcement is a flag flip, not a rework.
- **Scope boundary:** the rule covers first audio frame → hangup. Session *setup* may do
  synchronous reads (tenant config, cap check, consent state) — that is pre-budget.
- **Forward constraint:** any future mid-call state checkpointing (MVP-2 session continuity)
  inherits this rule — checkpoints are async best-effort, never awaited by a turn.
- Hot-path note: emission is an in-memory enqueue (~0ms); durability cost moves off-loop to the
  spool writer. Verified in staging by the collector-outage chaos gate (see `mvp1-environments`).

## Vendor-account runway as an SLO (downtime guard for accounts-payable)

> A funded vendor account (Deepgram / LiveKit / Cartesia / Claude / Vertex) is production
> infrastructure with a health check. A money event (prepaid balance → 0, declined auto-recharge,
> billing-account delinquency) must not silently become a live-call outage. The collector already
> knows spend-per-vendor; extend it to track headroom and alert ahead of depletion.

- **Metric: runway-in-days per vendor** = remaining prepaid balance / credit headroom ÷ current
  burn rate. Days (not dollars) so it auto-adjusts to traffic growth.
- **Alert thresholds: 14 / 7 / 3 days** of runway → page ops/finance to top up or approve the
  invoice *calmly, ahead of time*. Treat at the same tier as latency SLOs (see `observability`).
- **GCP billing account is a special case** (correlated failure): Vertex embeddings **and** the
  `europe-west3` runtime are billed to the same account, so a delinquency can suspend the whole
  project, not one leg. Monitor billing-account validity + payment-method status distinctly; use a
  dedicated account with a backup payment method.
- **Pairs with the runtime guard:** depletion that slips past these alerts surfaces at call time as
  payment-class API errors — handled by the distinct breaker state in `failover-baseline`.
- Operational levers (contracts → invoiced/committed terms, backup payment methods) live outside
  the spec; this captures only the *detection* requirement.
