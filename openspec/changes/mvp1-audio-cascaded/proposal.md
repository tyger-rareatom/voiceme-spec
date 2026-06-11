# Proposal: mvp1-audio-cascaded

## Why
The MVP-default voice runtime; fastest to ship, zero GPU ops.

## What Changes
Implement the cascaded pipeline behind the audio interface: LiveKit + Deepgram STT + Claude
(Haiku/Sonnet cost routing) + Cartesia TTS, with VAD turn-taking and barge-in.

## User-visible impact
Callers have a real-time, grounded spoken conversation with the tenant's agent.

## Rollback
Disable inbound sessions per tenant via flag.
