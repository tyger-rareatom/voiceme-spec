# Proposal: mvp1-caller-verification

## Status
**Phase: MVP 1 — Blocked by:** `mvp1-tenant-provisioning`, `mvp1-tenant-config-store`,
`mvp1-channel-ingress`, `mvp1-usage-metering`. **Prerequisite for:** `mvp2-action-packs` (no account
tool may run without a verified caller). **Market-leadership capability 1 of 3** (with
`mvp2-action-packs` and `mvp2-compliance-evidence`).

## Why
Today a session is created from a public `data-tenant` slug alone. That has two consequences:

1. **The agent cannot know who is speaking**, so it can only answer from documents. The costly support
   calls in fintech and telco are account-specific ("where is my transfer?"), and they need a verified
   caller before any account data is read.
2. **Anyone can start sessions against a tenant** and run up its minutes (denial-of-wallet).

Voice channels cannot use passwords or spoken PINs safely, and SIM-swap fraud is a leading route to
account takeover in African mobile money and banking. Mobile operators now expose network APIs (GSMA
Open Gateway / CAMARA (Linux Foundation telco API project)): **Number Verification** confirms the device
is using the SIM for a stated number; **SIM Swap** returns whether, or when, that number's SIM last
changed. Combined with a signed identity assertion from the tenant's own app, these give a verified
caller without asking for secrets. Global voice-agent platforms do not integrate operator APIs country by
country; this is a defensible VoiceMe capability.

## What Changes
- Add **signed session bootstrap**: account-capable tenants' sessions require a short-lived token signed
  by the tenant backend (JWT (JSON Web Token)) carrying a tenant-scoped user reference and scopes.
- Add a **caller assurance level** (L0–L3) computed per session and exposed to the runtime and to
  `mvp2-action-packs`.
- Add a **network identity provider interface** (operator or aggregator adapters behind one contract)
  for Number Verification and SIM Swap checks, with a one-time-code (OTP) fallback.
- Add **abuse controls** at session bootstrap: origin allowlist (web), per-tenant and per-source rate
  limits, and a per-tenant daily spend cap.

## User-visible impact
- Tenants configure their verification policy and signing keys in the portal.
- Callers in a tenant's app are verified silently; no PIN or password is spoken.
- A caller whose SIM changed recently is not given account information and is offered a human.

## Rollback
Per-tenant flag `caller_verification` in the tenant config store. Default `off` (knowledge-base answers
only, L0). Turning it off returns a tenant to MVP 1 behaviour; abuse controls stay on.
