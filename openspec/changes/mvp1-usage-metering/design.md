# Design: mvp1-usage-metering

## Approach
- High-throughput collector service (Go) ingesting usage events from every backend's mandatory
  usage callback. Durable store; near-real-time aggregation per tenant.
- Feeds (a) billing and (b) an internal **margin dashboard** (revenue vs vendor cost per tenant).
- Metering accuracy is a correctness requirement: reconciliation tests against vendor invoices.
