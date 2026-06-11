## ADDED Requirements

### Requirement: Self-serve tenant sign-up
The system SHALL allow a business to create a tenant account with email verification and provision
an isolated workspace identified by a unique `tenant_id`.

#### Scenario: New business signs up
- GIVEN a visitor with a valid business email
- WHEN they complete sign-up and verify their email
- THEN a tenant is created with a unique `tenant_id` and a branded subdomain is provisioned
- AND the visitor becomes the tenant's first admin user

### Requirement: Tenant isolation by construction
The system SHALL scope every stored object and data access by `tenant_id` such that no request
authenticated for tenant A can read or write tenant B's data.

#### Scenario: Cross-tenant access is impossible
- GIVEN an authenticated user of tenant A
- WHEN they request a resource belonging to tenant B (by id or by crafted query)
- THEN the system returns not-found/forbidden and logs the attempt
- AND no tenant B data is exposed

### Requirement: Role-based access within a tenant
The system SHALL support at least admin and member roles per tenant.

#### Scenario: Member cannot change billing
- GIVEN a member (non-admin) user
- WHEN they attempt to change the subscription tier
- THEN the action is denied
