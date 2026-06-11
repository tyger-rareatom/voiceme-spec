## ADDED Requirements

### Requirement: Channel-adapter seam
The system SHALL place a channel-ingress layer in front of the transport so that WebRTC, SIP, and
WhatsApp adapters present a uniform session to the audio runtime.

#### Scenario: WebRTC call enters via adapter
- GIVEN a caller on the web widget
- WHEN the call connects
- THEN a WebRTC adapter normalizes it into a uniform session for the audio runtime

#### Scenario: Unsupported channel fails cleanly
- GIVEN a channel with no implemented adapter (e.g., SIP in MVP 1)
- WHEN a connection is attempted
- THEN it is rejected with a clear "channel not enabled" response (no silent failure)
