# Design: mvp1-billing-subscription

## Approach
- Stripe subscriptions + metered usage records pushed from the metering plane.
- Entitlements map to tier; enforcement middleware in the control plane.
- Pricing = enterprise card from project.md (Starter $2–5k / Growth $10–20k / Scale $30–60k).
  The discarded $99/$499 placeholder pricing MUST NOT be implemented.

## Open gap: Stripe cannot collect from African tenants (payment-provider interface needed)

> Surfaced during exploration. This is a real MVP 1 contradiction, not a forward note: our tenants
> are African businesses, but the chosen biller can't onboard them.

- **Problem.** As of 2026, **Stripe does not directly support Nigeria or Kenya** as merchant
  countries — only via the Paystack "extended network" / merchant-of-record workaround. A Lagos or
  Nairobi tenant therefore cannot self-serve sign up and pay subscription + overage through vanilla
  Stripe. The business model (recurring subscription + metered overage) assumes a biller that can
  actually charge the target market.
- **Direction — billing-provider behind an interface** (same swappability principle as `audio_backend`
  / `rag_backend`): a `billing_provider` resolved per tenant, where the metering→biller overage push
  and the subscription/entitlement logic are provider-agnostic.
  - **Stripe** — global / non-African tenants.
  - **Paystack** (Stripe-owned; Nigeria, Ghana, South Africa, Kenya) or **Flutterwave** (15+ African
    countries) — African tenants; supports local methods (cards, bank transfer, USSD, mobile money).
- **Implications to resolve at build time:** overage metering must push to whichever provider a tenant
  is on; currency/settlement differs per provider; tier entitlements stay provider-agnostic (only the
  charge/collect leg varies). Verify subscription + usage-based billing primitives exist on the
  African provider chosen (recurring + metered), not just one-off charges.
