# Design: mvp3-nemotron-spike

## Approach
- Serve Nemotron Super via NIM, detailed-thinking-off, with the tool-call parser and chat template
  set explicitly (never defaults — this is where the field failures live). Pin the container version.
- Identical evaluation run against Claude as baseline; thresholds are relative (selection) and
  absolute (parse validity, discipline, latency).
- Effort: ~1 engineer, 1 week, rented GPU. The recorded decision (+ exact config on PASS) is the
  deliverable; the infrastructure is disposable.

## Gate integration
The PASS/FAIL flag is read by `mvp3-audio-nvidia`'s llm_slot guard and by the Phase 4
agentic-actions proposal as a hard prerequisite.
