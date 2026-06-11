## ADDED Requirements

### Requirement: Real-traffic trial before Scale commitment
The system SHALL support a time-boxed trial mode for prospective Scale tenants on real traffic,
producing a measured trial report.

#### Scenario: Trial produces evidence
- GIVEN a prospect in trial mode for the agreed window
- WHEN the window closes
- THEN a trial report is generated covering latency (p50/p95), cost per conversation, answer
  quality, and deflection rate

### Requirement: Commit gate
The system SHALL require a completed trial report before a Scale-tier pricing commitment is recorded.

#### Scenario: Commitment without trial blocked
- GIVEN a prospect with no completed trial report
- WHEN a Scale contract is attempted in the system
- THEN it is blocked pending the trial gate (override requires recorded executive exception)
