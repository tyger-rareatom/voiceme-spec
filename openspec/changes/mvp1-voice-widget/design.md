# Design: mvp1-voice-widget

## Approach
- Framework-free TypeScript bundle; reads `data-tenant`; establishes a session via the channel-ingress
  layer (WebRTC adapter). Branding/persona fetched per tenant. CDN-served, versioned, pinned.

## Ubiquity goal

- The widget is the product's "catch": the **same** embed must run everywhere a customer's users are —
  desktop browser, mobile web, and **inside the tenant's native Android / iOS apps**. Goal is one
  ubiquitous surface, not a web-only widget. All of these are WebRTC (browser↔cloud); no phone-network
  channel is involved in MVP 1 (PSTN/SIP/WhatsApp are MVP 2 — see `mvp1-channel-ingress` design).

## In-app embedding: WebView now, native SDK later (deliberate)

- **MVP 1 = WebView wrapper.** The widget runs inside a mobile-app WebView (per the `voice-widget`
  spec's "Mobile WebView support" requirement). Cheapest path: same `widget.js`, zero native work.
- **Known limitation:** WebView degrades exactly the things the cascaded runtime is graded on —
  microphone access, echo cancellation, and barge-in / VAD turn-taking are weaker than native, and
  call/interrupt behaviour can be flaky. This puts the p50 ≤ 1.5s turn target and barge-in quality at
  risk on in-app calls specifically.
- **Decision:** ship WebView first, but treat **native iOS/Android SDKs as a planned later upgrade**,
  not an accident to be discovered when a tenant reports worse in-app call quality than web. Trigger to
  revisit: in-app call-quality / barge-in metrics regressing vs web, or a tenant requiring native UX.
  Cost of native path = maintaining two additional SDKs.
