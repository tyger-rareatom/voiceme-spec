# Design: mvp1-failover-baseline

## Approach
- Health checks per dependency; circuit breaker + graceful path to escalation/callback.
- LiveKit reconnection + documented capacity headroom; SPOF analysis recorded.
- Leaves the failover-controller seam open for MVP 2's B→A backend failover.
