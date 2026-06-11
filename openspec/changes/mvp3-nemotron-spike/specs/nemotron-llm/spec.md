## ADDED Requirements

### Requirement: Tool-call reliability gate
Nemotron SHALL be greenlit for sovereign agentic use only if, on the fixed 50-scenario evaluation:
tool-selection accuracy is within 5 points of the Claude baseline AND argument JSON-parse validity
is ≥ 98% AND no-tool discipline is ≥ 95% AND added latency fits the turn budget.

#### Scenario: All thresholds met
- GIVEN the completed evaluation run
- WHEN all four thresholds are met
- THEN the gate is recorded PASSED with the exact serving configuration as the supported recipe
- AND llm_slot=nemotron becomes selectable for sovereign tenants

#### Scenario: Capability passes, plumbing fails
- GIVEN tool-selection accuracy passes but JSON-parse validity fails
- WHEN the result is reviewed
- THEN parser/template remediation is time-boxed and the evaluation re-run before a final decision

#### Scenario: Capability fails
- GIVEN tool-selection or multi-step accuracy fails the thresholds
- WHEN the result is reviewed
- THEN the gate is recorded FAILED; sovereign agentic actions remain on Claude; revisit at next
  Nemotron release

### Requirement: Evaluation set realism
The 50-scenario set SHALL be drawn from real consented support intents covering: single-tool,
multi-tool selection, forced tool, no-tool discipline, and multi-step chains.

#### Scenario: Eval set composition verified
- GIVEN the assembled evaluation set
- WHEN reviewed
- THEN all five categories are represented and scenarios trace to real intents
