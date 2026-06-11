# Proposal: mvp2-audio-gemini

## Status
**Phase: MVP 2 — Blocked by:** `mvp1-audio-backend-interface`, `mvp1-tenant-config-store`,
`mvp1-usage-metering` (must be archived first).

## Why
Premium audio path: Gemini Live native audio offers the lowest per-minute cost (~$0.025/min) and
strong latency for languages it natively covers. Value driver for Scale tier is **latency + data
residency, not cost** (per-turn context re-billing makes it cost-neutral on long calls).

## What Changes
Implement Gemini Live as a second audio backend behind the `audio_backend` interface, with a
covered-language guard that prevents selecting it for unsupported languages.

## User-visible impact
Eligible tenants get a lower-latency premium voice experience; unsupported-language tenants are
prevented from a degraded configuration.

## Rollback
Route affected tenants back to `cascaded` via the config flag; no platform changes to revert.
