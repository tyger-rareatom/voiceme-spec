# Proposal: mvp2-scale-trial-gating

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-usage-metering`, `mvp1-observability`, `mvp2-audio-gemini`.

## Why
Scale-tier promises (latency, language quality, cost) must be validated on the prospect's real
traffic before pricing commitments — accent/language handling in particular must be empirically
proven, not assumed.

## What Changes
Add a trial mode: time-boxed real-traffic evaluation with a measured trial report (latency, cost,
quality, deflection) and a commit gate before Scale pricing is contracted.

## User-visible impact
Prospective Scale tenants get a structured, evidence-based trial; the business avoids committing
pricing to unvalidated workloads.

## Rollback
Trial mode is a tenant state; exiting it reverts to standard onboarding.
