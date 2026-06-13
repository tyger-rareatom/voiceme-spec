# Proposal: mvp1-llm-routing-spike

## Status
**Phase: MVP 1 — Blocked by:** `mvp1-knowledge-ingestion`, `mvp1-rag-retrieval` (needs anchor-tenant
docs ingested + tenant-scoped retrieval to feed identical RAG context). **Informs** the LLM router in
`mvp1-audio-cascaded` and **pre-clears** the sovereign agentic gate in `mvp3-nemotron-spike`.

## Why
The cost-routing principle (trivial→cheap, substantive→anchor) currently assumes Claude Haiku/Sonnet,
and `project.md` flags Claude $/min as the most fragile unit-economics input. **Gemma 4 26B A4B** (MoE,
3.8B active, ~13× cheaper input than Haiku, function-calling, 140+ languages, **open weights**, available
serverless on **Vertex EU**) is a candidate cheap-tier — and, because it is open-weights, the *same* model
can later be self-hosted in-VPC, making it a low-risk sovereign LLM slot (vs the Nemotron gamble). But
public benchmarks don't tell us what matters for regulated fintech/telco voice: grounded-answer fidelity,
tool/escalation reliability, and behaviour on STT-style input. De-risk with a structured one-week spike
before steering routing or the sovereign path.

## What Changes
Run a structured evaluation of **Gemma 4 26B A4B (Vertex EU)** against a **Claude Haiku + Sonnet** baseline
on a frozen ~120-scenario grounded-support set (built from AcmePay/TelcoOne docs, fed STT-style input with
identical retrieved context), scoring grounding/faithfulness, refusal correctness, answer quality,
function-call reliability, escalation accuracy, latency, and measured cost/turn. Record a **routing-tier
verdict** (one-brain / two-brain / conservative / fail) and keep the frozen set + harness as a reusable
**LLM acceptance suite**. No production model change ships in this change — only the recorded verdict
and the suite.

## User-visible impact
None directly. Determines which model serves which turns (cost + quality), honestly gated.

## Rollback
N/A — the spike is disposable; only the recorded verdict and the reusable eval suite persist. The
`project.md` cost-routing/LLM lines are updated to reflect the verdict in a follow-up.
