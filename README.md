# VoiceMe — OpenSpec Spec Package

This package drives VoiceMe's architecture, planning, and development through
[OpenSpec](https://github.com/Fission-AI/OpenSpec) (spec-driven development).

## Files

| File | Purpose | Where it goes |
|---|---|---|
| `project.md` | The "worldview" — stack, architecture, principles, phase map, guardrails. OpenSpec injects this into every generated artifact. | `openspec/project.md` |
| `voiceme-phased-spec.md` | The full phased product spec. Each phase contains OpenSpec **changes** (proposal → spec delta with Given/When/Then → design → tasks). | Source for `openspec/changes/<change-id>/` |
| `README.md` | This guide. | — |

## How to use it

1. **Install + init OpenSpec** in your repo (requires Node.js ≥ 20.19):
   ```
   npx openspec init
   ```
2. **Drop in the foundation.** Replace `openspec/project.md` with this package's `project.md`.
   This is the single most important file — it stops the AI assistant from forgetting your stack
   and architecture mid-build.
3. **Work phase by phase, change by change.** OpenSpec's philosophy is *don't generate all specs
   upfront* — create each change when you're ready to build it. For each change in
   `voiceme-phased-spec.md`:
   - Run `/opsx:propose <change-id>` (e.g. `mvp1-usage-metering`) in your AI coding assistant, **or**
   - Scaffold the folder manually:
     ```
     openspec/changes/<change-id>/
       proposal.md      ← the proposal section
       specs/<capability>/spec.md   ← the spec-delta section (ADDED/MODIFIED Requirements)
       design.md        ← the design section
       tasks.md         ← the tasks checklist
     ```
   - Then `/opsx:apply` to implement, and `/opsx:archive` to fold the change into
     `openspec/specs/` (the source of truth) once shipped.

## Build order (do not reorder without reading Appendix B)

```
MVP 1  → Standard platform GA          (15 packages — fully scaffolded, build now)
MVP 2  → Premium / Scale + sovereign   (6 packages — scaffolded, BLOCKED-BY headers gate start)
MVP 3  → Africa language moat (NVIDIA)  (5 packages — scaffolded, BLOCKED-BY headers gate start)
Phase 4 → Agentic actions & intelligence (stub in master spec — expand at the time)
Phase 5 → Scale & expansion             (stub in master spec — expand at the time)
```

All 26 change packages live under `openspec/changes/`. **Every MVP 2/3 proposal carries a
`Status / Blocked-by` header** naming the prerequisite changes that must be archived first —
AI assistants must honor these (enforced in AGENTS.md).

**Hard prerequisites (Appendix B in the spec):**
- The `audio-backend` interface, `tenant-config-store`, and `usage-metering` (all MVP 1) must exist
  before any MVP 2/3 audio backend.
- `consent-capture` (MVP 1) must exist before MVP 3 language-pack data work.
- `mvp3-nemotron-spike` gates Phase 4 sovereign agentic actions AND `llm_slot=nemotron` selection.
- `mvp2-backend-failover` requires a second backend to exist (follows `mvp2-audio-gemini`).
- Scale-tier pricing commitments require `mvp2-scale-trial-gating` to have run.
- `mvp2-rag-vertex` task 1.1 (region availability check) is a hard gate — do it first.

## Why MVP 1 is bigger than it looks

MVP 1 deliberately includes the **operational spine** that a naive "voice MVP" omits but that this
product cannot ship without: usage **metering** (you're usage-priced), **failover** (voice is
real-time), **escalation + CRM** (already sold), **continuous-learning ingestion** (the
differentiator), **channel-ingress abstraction** (WhatsApp/SIP aren't WebRTC), **consent capture**
(the language-pack flywheel is also a legal pipeline), and the **audio-backend interface** (so MVP
2/3 slot in without forking). Resist the urge to defer these — retrofitting them is the expensive path.

## Suggested `openspec/config.yaml` rules

```yaml
schema: spec-driven
context: |
  See project.md. Multi-tenant voice-agent platform. Python 3.12 (LiveKit Agents) + Go
  (perf/devops services) + TypeScript/Next.js (portal/widget). Postgres+pgvector. GCP.
  Tenant isolation by tenant_id is non-negotiable. Usage metered from day one.
rules:
  proposal:
    - State user-visible impact and rollback strategy
  specs:
    - Use Given/When/Then scenarios
    - Every requirement must be testable
  design:
    - Note backend-interface conformance and tenant-isolation approach
    - Include a sequence note for any live-call hot-path change
  tasks:
    - Atomic, ~2-hour chunks, implementation-ready
    - Include a test task for any isolation- or metering-touching change
```
