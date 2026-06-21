# Design: mvp1-failover-baseline

## Approach

- Health checks per dependency; circuit breaker + graceful path to escalation/callback.
- LiveKit reconnection + documented capacity headroom; SPOF analysis recorded.
- Leaves the failover-controller seam open for MVP 2's B→A backend failover.

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
