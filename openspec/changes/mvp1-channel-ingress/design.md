# Design: mvp1-channel-ingress

## Approach
- Uniform session abstraction; WebRTC adapter over LiveKit.
- SIP/WhatsApp adapters are interface stubs documented for MVP 2/3 — they exist so the seam is real,
  and they answer connections with an explicit not-enabled response.

## Forward note: carrier candidates for the SIP/WhatsApp adapters (MVP 2)

> Captured during exploration; not MVP 1 scope. Propose properly when PSTN/WhatsApp is reached
> (per the spec's "create specs as needed, not upfront" philosophy). MVP 1 stays WebRTC-only.

- **When these adapters are built (MVP 2 — PSTN phone numbers / "dial a real number", SIP trunking
  for telco tenants, and WhatsApp), Telnyx is a strong candidate carrier.** It owns its own network
  (cheaper PSTN minutes than Twilio/Vonage) and has confirmed DID + SIP coverage in the target
  markets — Nigeria, Kenya, South Africa, Tanzania, Uganda, Rwanda (Nigeria allows unlimited DIDs on
  one SIP trunk).
- **Boundary — carrier, never the brain.** Telnyx fits *behind* the channel-ingress adapter, carrying
  the call into our uniform session. It must **not** replace the media stack (Deepgram STT / Claude
  routing / Cartesia TTS) or the RAG path. Their bundled "Voice AI" (STT+LLM+TTS on one per-minute
  price, GPT-5.4 hosted) is explicitly out: it would collapse per-component metering (a correctness
  requirement — see `usage-metering`), erase the Haiku/Sonnet cost-routing lever, and concede the
  MVP 3 language moat (self-hosted Riva + Pidgin/Swahili).
- **Tier limit — Standard only.** Telnyx is US-HQ with EU-deployed infra; routing audio through it
  likely conflicts with the MVP 2 sovereign in-region residency posture (NDPR/POPIA/SARB, BYOK).
  Scale/Sovereign tenants need a region-appropriate carrier, so keep the adapter **vendor-agnostic**
  (Telnyx as one implementation, not the interface). Also: each African DID carries per-country
  KYC/regulatory documentation requirements — onboarding friction to scope at proposal time.
- **Second carrier candidate — Africa's Talking (the residency-grade impl).** Where Telnyx fails the
  residency test (MVP 2 Scale/Sovereign tenants under NDPR/POPIA), **Africa's Talking** is the
  in-region answer: voice + SIP endpoints, WhatsApp, SMS/USSD across Kenya, Nigeria and East/West
  Africa, with local regulatory presence. Natural split: **Telnyx for cost on Standard tier,
  Africa's Talking for residency on Sovereign tier** — which is exactly why the adapter stays
  vendor-agnostic (two impls behind one interface). Verify at proposal time: real-time media-stream
  quality for live AI turns (its Voice API is call/IVR-oriented; confirm it meets the barge-in +
  p50 ≤ 1.5s budget) and WhatsApp BSP terms.
- **Other carriers to weigh:** Twilio / Infobip / Sinch / Vonage / Plivo (Infobip notable for
  in-region data centers → residency). Bundled voice-agent platforms (Vapi / Bland / Retell, and
  Telnyx's own Voice AI tier) are **anti-fits** — same black-box trap as above; study as competitors,
  never adopt as the runtime.
- **Real comparison at proposal time:** Telnyx vs **LiveKit SIP** (already in the stack) + a number
  provider, for the telephony adapter specifically — not "Telnyx vs our media stack".
