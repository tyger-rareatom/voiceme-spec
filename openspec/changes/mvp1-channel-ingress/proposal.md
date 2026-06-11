# Proposal: mvp1-channel-ingress

## Why
Web/mobile use WebRTC, but WhatsApp and IVR-replacement (SIP) do not. Building the adapter seam now
means later channels don't require runtime surgery.

## What Changes
Add a channel-ingress layer presenting a uniform session to the audio runtime; implement WebRTC now;
stub SIP + WhatsApp adapters with explicit not-enabled behavior.

## User-visible impact
Widget works on web/mobile; future channels slot in cleanly.

## Rollback
Only WebRTC enabled.
