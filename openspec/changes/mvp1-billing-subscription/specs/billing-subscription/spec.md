## ADDED Requirements

### Requirement: Plan subscription
The system SHALL support Standard, Regulated and Sovereign plan subscriptions with prices read from the
tenant's pinned pricing-catalogue version, enforcing plan entitlements.

#### Scenario: Plan gates features
- GIVEN a Standard subscription
- WHEN the tenant attempts a Regulated-only feature (for example complaint cases)
- THEN it is gated with an upgrade prompt

### Requirement: Metered usage billing
The system SHALL bill final resolutions, minutes above the fair-use pool and modules using metering
data, at the tenant's pinned catalogue prices.

#### Scenario: Usage billed
- GIVEN a tenant with final resolutions and minutes over its pool in the period
- WHEN the billing period closes
- THEN resolutions and overage are charged at the tenant's catalogue prices
