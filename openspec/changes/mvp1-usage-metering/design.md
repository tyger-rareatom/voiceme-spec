# Design: mvp1-usage-metering

## Approach

- High-throughput collector service (Go) ingesting usage events from every backend's mandatory
  usage callback. Durable store; near-real-time aggregation per tenant.
- Feeds (a) billing and (b) an internal **margin dashboard** (revenue vs vendor cost per tenant).
- Metering accuracy is a correctness requirement: reconciliation tests against vendor invoices.

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
