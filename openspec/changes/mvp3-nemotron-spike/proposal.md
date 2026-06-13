# Proposal: mvp3-nemotron-spike

## Status
**Phase: MVP 3 — Blocked by:** `mvp3-gpu-ops` (serving substrate). **This change IS the gate** for
Phase 4 sovereign agentic actions and for `llm_slot=nemotron` selection.

## Why
A fully in-VPC tool-calling stack (Riva + Nemotron + Magpie) is the sovereign agentic story — but
field reports show Nemotron tool-calling is sensitive to parser/template configuration (raw-JSON
emissions, template bugs) and requires detailed-thinking-off. De-risk with a one-week spike before
any roadmap commitment depends on it.

**Note (open-weights alternative):** `mvp1-llm-routing-spike` evaluates **Gemma 4 26B A4B** — open
weights, function-calling, multilingual — on the *same* function-call thresholds used here. If Gemma
passes there, it becomes a greenlit open-weights sovereign LLM-slot candidate (self-hosted in-VPC),
and this spike narrows to a Nemotron-specific cost/perf optimization rather than a hard gate. Consider
reframing as an "open sovereign LLM slot" evaluation (Gemma vs Nemotron) when reached.

## What Changes
Run a structured spike: serve Nemotron Super via NIM with explicit tool-call parser + chat template,
evaluate on a fixed 50-scenario tool-calling set drawn from real consented intents, against a Claude
baseline, and record a PASS/FAIL gate decision.

## User-visible impact
None directly; gates future sovereign agentic capability honestly.

## Rollback
N/A — the spike is disposable by design; only the recorded gate decision persists.
