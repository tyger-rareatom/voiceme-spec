# Proposal: mvp3-swahili-pack

## Status
**Phase: MVP 3 — Blocked by:** `mvp3-pidgin-pack` (reuses the workstream pattern + tooling),
`mvp3-audio-nvidia`.

## Why
Swahili opens the East Africa expansion (Kenya/Tanzania; M-Pesa, Safaricom, regional banks).
Second pack validates that the language-pack workstream is repeatable — the moat scales.

## What Changes
Replicate the Pidgin workstream for Swahili: style guide, data acquisition, ASR fine-tune, custom
voice, eval, regional routing.

## User-visible impact
Swahili-speaking callers get accurate recognition and a natural Swahili agent voice.

## Rollback
Swahili tenants revert to best-available covered-language backend; weights versioned.
