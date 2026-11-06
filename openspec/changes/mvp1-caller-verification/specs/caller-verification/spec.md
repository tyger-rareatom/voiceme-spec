## ADDED Requirements

### Requirement: Signed session bootstrap
The system SHALL require, for any tenant with `caller_verification` enabled, a session token signed with
a key registered to that tenant, carrying a tenant-scoped user reference, scopes, and an expiry of no
more than 5 minutes. The system SHALL reject expired, unsigned, replayed, or wrongly signed tokens.

#### Scenario: Valid tenant token starts a verified-capable session
- GIVEN AcmePay has `caller_verification` enabled and a registered signing key
- WHEN the widget calls session bootstrap with a token signed by that key, unexpired and unused
- THEN a session is created bound to AcmePay and to the token's user reference
- AND the session starts at assurance level L1

#### Scenario: Token from another tenant is rejected
- GIVEN a token correctly signed by TelcoOne's key
- WHEN it is presented in a session bootstrap for AcmePay
- THEN the request is rejected as unauthorized
- AND no session, LiveKit room, or metering record is created for either tenant
- AND the attempt is logged against AcmePay without exposing TelcoOne data

#### Scenario: Replayed token is rejected
- GIVEN a token that has already started a session
- WHEN the same token is presented again
- THEN the request is rejected

### Requirement: Caller assurance levels
The system SHALL assign each session exactly one assurance level from L0 (anonymous), L1
(tenant-asserted), L2 (number verified) and L3 (number verified with no recent SIM change), and SHALL
expose the current level to the runtime and to the action layer.

#### Scenario: Levels are earned in order
- GIVEN a session with no tenant token
- THEN it is L0
- WHEN a valid signed tenant token is presented it becomes L1
- WHEN the operator confirms the device's SIM matches the user's number, or a one-time code to that number succeeds, it becomes L2
- WHEN the operator reports no SIM change within the tenant's window it becomes L3

#### Scenario: Unverified caller asks an account question
- GIVEN a session at L0
- WHEN the caller asks for their transfer status
- THEN the agent does not call any account tool
- AND it explains it can help with general questions and offers sign-in or a human

#### Scenario: Recent SIM change blocks account access
- GIVEN a session at L2 and a tenant SIM-change window of 72 hours
- WHEN the operator reports the number's SIM changed 20 hours ago
- THEN the session does not reach L3
- AND money-related tools are unavailable for the session
- AND the agent offers a human hand-off without stating the reason as fraud

### Requirement: Network identity checks behind a provider interface
The system SHALL perform Number Verification and SIM Swap checks only through a
`network_identity_provider` interface, resolved per operator, so that operators and aggregators are
swappable. The system SHALL NOT call any operator or aggregator SDK from business logic.

#### Scenario: Operator without network APIs
- GIVEN a caller whose operator has no available provider
- WHEN verification is attempted
- THEN the system falls back to the tenant's configured fallback (one-time code or L1 only)
- AND records which method set the assurance level

#### Scenario: Provider timeout does not stall the call
- GIVEN the provider does not respond within its timeout
- WHEN the caller is speaking with the agent
- THEN the conversation continues at the current assurance level
- AND no turn waits on the provider beyond its timeout

### Requirement: Verification is metered
The system SHALL emit a usage event for every network identity check and every one-time code sent,
tagged with tenant, session, provider, and outcome.

#### Scenario: Un-metered verification path is rejected
- GIVEN a provider adapter that does not emit the usage callback
- WHEN it is registered
- THEN registration fails conformance and the adapter cannot be selected

### Requirement: Session abuse controls
The system SHALL enforce, at session bootstrap and before any media resources are allocated: an origin
allowlist for web embeds, per-tenant and per-source rate limits, and a per-tenant daily spend cap.

#### Scenario: Embed on an unlisted site
- GIVEN AcmePay's allowlist contains only its own domains
- WHEN `widget.js` with `data-tenant="acmepay"` loads on an unlisted domain and requests a session
- THEN the request is rejected and no minutes are consumed

#### Scenario: Daily spend cap reached
- GIVEN a tenant has reached its configured daily spend cap
- WHEN a new session is requested
- THEN the tenant's cap policy applies (reject with a clear message, or allow and alert)
- AND sessions already in progress are not cut off

### Requirement: Identity data minimisation
The system SHALL store verification outcomes (method, level, timestamp, provider) per session, and SHALL
NOT store full phone numbers in logs, telemetry, or transcripts; numbers are masked or hashed with a
per-tenant key.

#### Scenario: Phone number absent from telemetry
- GIVEN a completed verified session
- WHEN its logs, traces, and transcript are inspected
- THEN no full phone number appears in any of them
