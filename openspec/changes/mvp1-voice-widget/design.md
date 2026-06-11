# Design: mvp1-voice-widget

## Approach
- Framework-free TypeScript bundle; reads `data-tenant`; establishes a session via the channel-ingress
  layer (WebRTC adapter). Branding/persona fetched per tenant. CDN-served, versioned, pinned.
