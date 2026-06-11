# Design: mvp2-isolation-hardening

## Approach
- Provisioning modes: shared (default) vs dedicated (sovereign). Dedicated = per-tenant VPC, compute
  pool, and stores; pairs with sovereign-deployment topology.
- Shared-infra fairness: per-tenant rate/concurrency quotas at ingress; resource limits in the
  runtime; quota breaches degrade the offender, never the neighbour.
- Promote the MVP 1 cross-tenant test suite into a CI release gate; extend it to cover the new
  backends and stores as they land.
