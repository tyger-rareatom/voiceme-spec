# Proposal: mvp2-backend-failover

## Status
**Phase: MVP 2 — Blocked by:** `mvp2-audio-gemini` (a second backend must exist), `mvp1-failover-baseline`.

## Why
With two live backends, real failover becomes possible — and necessary. Gemini is a closed external
dependency; when it degrades, calls must continue on the cascaded stack rather than fail.

## What Changes
Add a failover controller that detects Gemini backend failure/degradation and fails sessions over to
the cascaded backend.

## User-visible impact
Callers experience continuity (possibly with a brief transition) instead of dropped calls during a
backend outage.

## Rollback
Failover controller disabled → baseline graceful-degradation behavior from MVP 1 applies.
