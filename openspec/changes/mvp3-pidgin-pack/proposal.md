# Proposal: mvp3-pidgin-pack

## Status
**Phase: MVP 3 — Blocked by:** `mvp1-consent-capture` (data source), `mvp3-audio-nvidia` (serving
substrate). **Critical path is DATA, not code.**

## Why
Nigerian Pidgin is the language moat: closed models (Gemini) cannot host it; owning fine-tuned
ASR/TTS weights makes it defensible. Pidgin v1 (prompt-steered on cascaded) ships earlier for
demos; this change delivers Pidgin v2 — the owned pack.

## What Changes
Deliver the full pack: locked transcription style guide → labelled data acquisition (~100–300 hrs)
→ Parakeet/Canary ASR fine-tune → custom Magpie Pidgin voice → eval harness → tenant routing.

## User-visible impact
Pidgin-speaking callers get accurate recognition and a genuine Nigerian Pidgin agent voice.

## Rollback
Pidgin tenants revert to v1 (prompt-steered cascaded); fine-tuned weights are versioned and
roll back independently.
