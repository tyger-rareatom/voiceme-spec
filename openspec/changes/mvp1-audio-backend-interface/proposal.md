# Proposal: mvp1-audio-backend-interface

## Why
Building the abstraction now (even with one backend) is what prevents forked codebases when Gemini
(MVP 2) and NVIDIA self-host (MVP 3) arrive. "Swap the engine, not the car."

## What Changes
Define the `audio_backend` interface (session lifecycle + mandatory usage callback) and the
per-tenant flag resolved by the Tenant Config Router at session setup.

## User-visible impact
None directly; enables MVP 2/3 backends without platform rewrites.

## Rollback
Single backend remains; interface is internal.
