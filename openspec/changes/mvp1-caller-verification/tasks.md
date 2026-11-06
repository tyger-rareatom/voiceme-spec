# Tasks: mvp1-caller-verification

## 1. Abuse controls
- [ ] 1.1 Origin allowlist per tenant (config schema + bootstrap check)
- [ ] 1.2 Per-tenant and per-source rate limiting at bootstrap
- [ ] 1.3 Daily spend cap read from metering + cap policy (reject / allow-and-alert)

## 2. Signed session bootstrap
- [ ] 2.1 Tenant signing-key registration (JWKS URL or upload) in the portal + tenant config store
- [ ] 2.2 Token validation (signature, `exp` ≤ 5 min, tenant match, scopes)
- [ ] 2.3 Single-use `jti` replay store with short TTL
- [ ] 2.4 Widget: accept a tenant-supplied token callback and pass it to bootstrap

## 3. Assurance levels
- [ ] 3.1 Assurance state machine (L0–L3) in the session runtime, readable by the action layer
- [ ] 3.2 Agent behaviour at L0/L1 for account questions (refuse tools, offer sign-in or human)

## 4. Network identity provider
- [ ] 4.1 `network_identity_provider` interface + stub implementation
- [ ] 4.2 First operator adapter (Number Verification + SIM Swap, CAMARA-shaped)
- [ ] 4.3 OTP fallback via SMS vendor behind the same interface
- [ ] 4.4 Async verification after connect; timeout + fallback handling
- [ ] 4.5 Usage callback for every check and OTP + conformance test (un-metered adapter rejected)

## 5. Privacy
- [ ] 5.1 Per-tenant keyed hashing of numbers; masking in logs, traces, transcripts

## 6. Tests
- [ ] 6.1 Cross-tenant denial test (tenant B token never opens tenant A session)
- [ ] 6.2 Replay, expiry, and wrong-key rejection tests
- [ ] 6.3 SIM-change-within-window test blocks L3 and money tools
- [ ] 6.4 Provider timeout test: no turn waits beyond timeout
- [ ] 6.5 Telemetry scan test: no full phone number in logs, traces, transcripts
- [ ] 6.6 Bootstrap latency instrumentation per stage
