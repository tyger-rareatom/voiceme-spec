## ADDED Requirements

### Requirement: Single-snippet embed
The system SHALL provide one `widget.js` that renders a tenant's branded voice widget based solely
on the `data-tenant` attribute, with no cross-tenant data leakage.

#### Scenario: Two tenants, same script
- GIVEN AcmePay and TelcoOne each embed widget.js with their own data-tenant
- WHEN each site loads
- THEN each shows its own branding/agent and connects only to its own tenant session

### Requirement: Mobile WebView support
The system SHALL function inside a mobile-app WebView, not only desktop browsers.

#### Scenario: Widget in a WebView
- GIVEN a mobile app embedding the widget in a WebView
- WHEN a user starts a voice session
- THEN the session functions equivalently to desktop web
