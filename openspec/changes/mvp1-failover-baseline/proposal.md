# Proposal: mvp1-failover-baseline

## Why
Real-time voice cannot have silent single points of failure; a hung call is worse than a failed one.

## What Changes
Add dependency health checks, circuit breakers, a graceful call-failure path to escalation, and
LiveKit transport-resilience basics. (Backend-to-backend failover arrives in MVP 2 when a second
backend exists.)

## User-visible impact
Fewer dropped calls; graceful degradation instead of dead air.

## Rollback
N/A (additive).
