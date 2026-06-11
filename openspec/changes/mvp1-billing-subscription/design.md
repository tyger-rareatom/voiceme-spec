# Design: mvp1-billing-subscription

## Approach
- Stripe subscriptions + metered usage records pushed from the metering plane.
- Entitlements map to tier; enforcement middleware in the control plane.
- Pricing = enterprise card from project.md (Starter $2–5k / Growth $10–20k / Scale $30–60k).
  The discarded $99/$499 placeholder pricing MUST NOT be implemented.
