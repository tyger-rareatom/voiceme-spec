# Design: mvp3-gpu-ops

## Approach
- NIM orchestration on the chosen GPU substrate (DGX Cloud rental first; owned capex later if
  volume justifies). Concurrency model documented: streams-per-GPU by model, headroom policy.
- Autoscaling keyed to concurrent sessions (not CPU); scale-up SLO agreed with product.
- MLOps: model registry, versioned deploys, canary + rollback.
- Cost telemetry: GPU-hour attribution per session → metering schema → margin dashboard, feeding the
  inflection computation (the same number that decides A/B → C routing).

## Staffing note (binding)
This workstream requires dedicated platform engineering. The single-engineer dependency on the
platform role is a known risk — the backup reserve from the budget MUST be active before this starts.
