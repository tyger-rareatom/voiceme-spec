# Design: mvp1-failover-baseline

## Approach

- Health checks per dependency; circuit breaker + graceful path to escalation/callback.
- LiveKit reconnection + documented capacity headroom; SPOF analysis recorded.
- Leaves the failover-controller seam open for MVP 2's B→A backend failover.

## Decision (2026-07-07): degrade gracefully — no second TTS vendor in MVP 1

- On vendor failure the MVP-1 behaviour is **graceful degradation** (spoken failure message,
  escalation, callback offer), **not** same-turn failover to an alternate TTS vendor.
- **Rejected alternative — "stay speaking" multi-vendor TTS failover** (from the scalability
  proposal review): tripping to a fallback TTS vendor keeps the agent talking through an outage,
  but requires a second TTS contract, EU-endpoint pinning, and voice-parity work at MVP-1 traffic
  levels. Revisit at MVP 2 alongside B→A backend failover, where an alternate backend (with its
  own TTS) exists anyway and the breaker's "drain to alternate" hook takes over this job.
- Consequence for the breaker: its purpose at MVP 1 is **bounding caller-perceived silence** —
  detect fast (2 sequential timeouts or >800ms hot-path latency) and hand off to the graceful
  path fast. Trip thresholds live in config (per dependency), not code.
- Hot-path note: the breaker state check is an in-memory read (~0ms). The latency-budget win is
  on the failure path — an open breaker replaces stacked vendor timeouts (multi-second) with an
  immediate graceful turn, keeping even failure turns inside the budget.

## Payment-class errors are a distinct breaker state (not a transient outage)

> A vendor cutting access for a money reason (prepaid balance exhausted, declined recharge, spend
> cap hit) returns `402 / 401 / quota-429`. This is **persistent and account-wide**, unlike a
> transient `503`/timeout — so the normal trip→retry→half-open recovery is wrong: retrying just
> hammers a vendor that will not answer until the account is paid, producing the dead-air this
> capability exists to prevent.

- **Classify `402 / 401 / quota-429` as a separate breaker state** from transient faults.
  Transient → trip, retry, half-open, recover. Payment-class → trip and **stop retrying** until
  cleared.
- **On payment-class trip:** page ops/finance immediately (it is an accounts-payable incident, not
  a vendor outage), and degrade the affected call gracefully (spoken failure / escalation /
  callback) exactly as for any dependency fault — never dead air.
- **MVP 2 hook:** once B→A backend failover exists, a payment-class trip should **drain traffic to
  the alternate backend** until the account is resolved, rather than half-open-retrying the
  unpaid vendor.
- **Detection upstream:** vendor-account runway alerts (see `usage-metering`) should make this state
  rare — by the time a call hits a `402`, the 14/7/3-day warnings were already missed.
