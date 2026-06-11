# Proposal: mvp3-audio-nvidia

## Status
**Phase: MVP 3 — Blocked by:** `mvp1-audio-backend-interface`, `mvp1-usage-metering`,
`mvp3-gpu-ops` (deploys the serving substrate; build together).

## Why
The self-hosted NVIDIA Riva path is the substrate for the language moat (own the ASR/TTS weights →
fine-tune for Pidgin/Swahili) and completes the sovereign story (in-VPC speech processing). It only
pencils out at volume — routing must enforce the inflection rule.

## What Changes
Implement the NVIDIA backend behind `audio_backend`: Parakeet/Canary ASR + Magpie TTS served via
self-hosted NIM, with a swappable LLM slot (Claude default ⇄ Nemotron, spike-gated).

## User-visible impact
Language-pack tenants get Africa-native speech; sovereign tenants get in-VPC speech processing.

## Rollback
Per-tenant flag back to cascaded/gemini; NIM deployment torn down independently of the platform.
