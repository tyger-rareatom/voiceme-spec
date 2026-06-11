# Design: mvp1-channel-ingress

## Approach
- Uniform session abstraction; WebRTC adapter over LiveKit.
- SIP/WhatsApp adapters are interface stubs documented for MVP 2/3 — they exist so the seam is real,
  and they answer connections with an explicit not-enabled response.
