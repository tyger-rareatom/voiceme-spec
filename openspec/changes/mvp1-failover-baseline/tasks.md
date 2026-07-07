# Tasks: mvp1-failover-baseline

## 1. Dependency resilience
- [ ] 1.1 Dependency health checks + circuit breakers
- [ ] 1.2 Graceful call-failure path → escalation/callback
- [ ] 1.3 Per-dependency breaker thresholds in config (2-sequential-timeout + latency ms, TTS default 800ms) with half-open recovery
- [ ] 1.4 Breaker fail-fast test: open breaker → graceful path within turn budget, no vendor call attempted

## 2. Transport
- [ ] 2.1 LiveKit reconnection + capacity headroom
