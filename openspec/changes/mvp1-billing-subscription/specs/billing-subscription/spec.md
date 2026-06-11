## ADDED Requirements

### Requirement: Tiered subscription
The system SHALL support Starter/Growth/Scale subscriptions with the operative enterprise pricing,
enforcing tier entitlements.

#### Scenario: Tier gates features
- GIVEN a Starter subscription
- WHEN the tenant attempts a Growth-only feature
- THEN it is gated with an upgrade prompt

### Requirement: Metered overage billing
The system SHALL bill overage beyond tier caps using metering data.

#### Scenario: Overage billed
- GIVEN a tenant exceeding its cap with bill-overage policy
- WHEN the billing period closes
- THEN overage is charged per the published overage rate
