## ADDED Requirements

### Requirement: LLM routing-tier verdict gate
The system SHALL set each turn-class's model (trivial / substantive / hard-escalation) only from a
recorded verdict of the frozen evaluation, scored against a Claude Haiku + Sonnet baseline. Gemma's
production routing share SHALL NOT exceed what its measured results support.

#### Scenario: Two-brain verdict
- GIVEN the completed evaluation
- WHEN Gemma meets the safety floor AND its grounding + answer-quality are within ~3 points of Sonnet
  AND the function-call gate passes
- THEN the verdict is recorded "two-brain": Gemma serves trivial + substantive turns, Sonnet is reserved
  for hard/regulated/escalation turns, and the router tier map is set accordingly

#### Scenario: Conservative verdict
- GIVEN the completed evaluation
- WHEN Gemma beats/ties Haiku at the safety floor but does NOT reach within ~3 points of Sonnet on
  substantive grounding/quality
- THEN the verdict is recorded "conservative": Gemma replaces Haiku for trivial turns only; Sonnet keeps
  substantive turns

#### Scenario: Fail verdict
- GIVEN the completed evaluation
- WHEN Gemma misses the grounding/safety floor
- THEN the verdict is recorded "fail": routing stays Claude-only and Gemma is revisited at its next release

### Requirement: Grounding and safety floor
The system SHALL require Gemma to meet an absolute grounding/safety floor before any production routing:
≥ 98% no-hallucination on the grounded set, ≥ 95% correct refusal on the out-of-scope set, and a clean
pass on the adversarial/safety set (including doc-borne prompt-injection).

#### Scenario: Floor not met blocks all routing
- GIVEN Gemma's evaluation results
- WHEN any floor metric is missed
- THEN Gemma is not routed for production turns regardless of its cost or latency advantage

### Requirement: Function-call reliability shared with the sovereign gate
The evaluation SHALL score Gemma's function-calling on the same thresholds as the Nemotron sovereign
gate: tool-selection accuracy within 5 points of the Claude baseline AND argument JSON-parse validity
≥ 98% AND no-tool discipline ≥ 95%.

#### Scenario: Function-call pass pre-clears the sovereign slot
- GIVEN Gemma passes the function-call thresholds
- WHEN the result is recorded
- THEN it is referenced by `mvp3-nemotron-spike` as evidence that Gemma is a greenlit open-weights
  sovereign LLM-slot candidate (self-hosted), reducing dependence on Nemotron

### Requirement: Nigerian-Pidgin base-vs-tuned adequacy verdict
The evaluation SHALL include a genuine Nigerian-Pidgin subset (not merely light code-switch) and SHALL
record an explicit verdict on whether **base** Gemma is adequate for Pidgin, or whether a fine-tuned
Pidgin LoRA adapter is warranted. The verdict gates whether any Pidgin-tuning workstream is started.

#### Scenario: Base Gemma adequate on Pidgin
- GIVEN the Pidgin subset results for base Gemma
- WHEN base Gemma meets the grounding/quality floor on genuine Pidgin
- THEN the verdict is "base adequate"; no Pidgin tune is started and the saving is banked (revisit on
  tenant demand)

#### Scenario: Pidgin gap warrants a tune
- GIVEN base Gemma misses the floor on the genuine Pidgin subset
- WHEN the gap is recorded
- THEN a Pidgin LoRA adapter is justified — but it is built only when a channel can deliver its value
  (text channel, or MVP-3 speech models), since a tuned model is a deployed endpoint with ongoing cost

### Requirement: Evaluation-set realism and reuse
The evaluation set SHALL be a frozen ~120-scenario set drawn from real anchor-tenant documents, fed as
STT-style input (disfluent, unpunctuated, accented) with identical retrieved context across models, and
SHALL be retained as a reusable LLM acceptance suite.

#### Scenario: Eval set composition verified
- GIVEN the assembled evaluation set
- WHEN reviewed
- THEN all seven categories are represented (grounded, out-of-scope, tool-requiring, no-tool, escalation,
  multilingual/code-switch, adversarial/safety), input is STT-style, and retrieved context is identical
  per scenario across the three models

#### Scenario: Suite reused at the sovereign transition
- GIVEN a later managed→self-hosted Gemma deployment (MVP 3)
- WHEN behavioural parity must be confirmed
- THEN the same frozen suite is re-run and parity is asserted against the recorded managed baseline
