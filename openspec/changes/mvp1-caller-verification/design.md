# Design: mvp1-caller-verification

## Approach
- **Session bootstrap service** (FastAPI, control plane) gains three stages before a LiveKit token is
  minted: (1) abuse controls, (2) tenant-token validation, (3) assurance-level initialisation. Media
  resources are allocated only after stage 1 passes.
- **Tenant tokens:** tenants register public keys (JWKS (JSON Web Key Set) URL or uploaded key) in the
  portal. Tokens carry `tenant_id`, `sub` (tenant-scoped user reference, opaque to VoiceMe), `scopes`,
  `exp` (≤ 5 min), `jti` (single use). `jti` is held in a short-TTL store for replay detection.
- **Assurance state machine** lives in the session runtime: `L0 → L1` at bootstrap; `L1 → L2 → L3`
  asynchronously. The current level is readable by `mvp2-action-packs`' policy check; it never decreases
  mid-session except on an explicit downgrade event (e.g. provider reports a SIM change).
- **Network identity provider interface** (`network_identity_provider`):
  - `verify_number(session, msisdn_ref) -> Result{matched|not_matched|unavailable}`
  - `sim_swap(session, msisdn_ref, window_hours) -> Result{swapped_at|none|unavailable}`
  - `send_otp / check_otp` for the fallback (wraps the SMS vendor).
  - Implementations: one operator adapter (first target operator, CAMARA-shaped), one aggregator adapter,
    and a stub for tests. Operator resolution must not rely on number prefix alone (number portability);
    use the provider's lookup where available.
- **Abuse controls:** origin allowlist checked on the bootstrap request's `Origin` (web only); native
  apps cannot be trusted on `Origin`, so mobile tenants rely on the signed token, optionally with app
  attestation tokens passed through. Rate limits use a per-tenant and per-source token bucket. The spend
  cap reads the tenant's running cost from the metering plane.

## Channel notes
- **In-app widget (WebRTC):** Number Verification works only when the device is on mobile data with the
  SIM; on Wi-Fi it returns unavailable, and the OTP fallback applies.
- **Phone (SIP, MVP 2 adapters):** caller ID can be spoofed, so caller ID alone never exceeds L1-equivalent.
  SIM Swap on the caller-ID number still applies as a risk signal; OTP is the step-up.
- **WhatsApp (MVP 2 adapters):** the WhatsApp number is a tenant-asserted identity at best (L1); step-up
  by OTP.

## Tenant isolation
- Signing keys, verification policy, and outcomes are stored through the tenant-scoped repository layer.
- `msisdn_ref` is a per-tenant keyed hash; the raw number is passed only to the provider call and held in
  memory for the session.
- Cross-tenant denial test: a token signed by tenant B never creates a session for tenant A (spec scenario).

## Hot-path sequence note
Bootstrap (before media): allowlist → rate limit → spend cap → token verify (local key cache, target
< 20 ms) → mint LiveKit token. Network checks start **after** connect, in parallel with the greeting, and
are off the turn path: no turn waits for them. A tool that requires L2/L3 waits for the result up to the
provider timeout (default 3 s, not yet measured) while the agent speaks a holding phrase; on timeout the
tool is refused with the fallback offer. **Expected impact on the ≤ 1.5 s p50 turn budget: none for turns
that do not call account tools.** Instrument bootstrap stages and provider latency as separate segments.

## Vendor interfaces wrapped
`network_identity_provider` (operators, aggregators), SMS vendor behind the same interface for OTP.

## Open validation
- Which operators in the first target country expose live Number Verification and SIM Swap, at what
  price per call, and with what end-user consent requirements.
- Provider latency at p50/p95 from the Frankfurt control plane.
