# Tasks: mvp1-llm-routing-spike

## 1. Eval set & harness
- [ ] 1.1 Assemble frozen ~120-scenario set from anchor-tenant docs across the 7 categories
- [ ] 1.2 Capture STT-style variants (disfluent, unpunctuated, accented) for each scenario
- [ ] 1.3 Include a genuine Nigerian-Pidgin subset (not just light code-switch) in the multilingual slice
- [ ] 1.4 Pin identical retrieved context per scenario (hold RAG fixed); label tool/escalation ground truth
- [ ] 1.5 Build the harness (blind judge + deterministic scorers + cost/latency capture)

## 2. Runs
- [ ] 2.1 Run Gemma 4 26B A4B (Vertex EU), Haiku, and Sonnet over the frozen set (≥3 runs, fixed temp)
- [ ] 2.2 Score all metrics; human spot-check a stratified sample per category

## 3. Decision
- [ ] 3.1 Record the routing-tier verdict (one-brain / two-brain / conservative / fail) + evidence
- [ ] 3.1a Record the Pidgin base-vs-tuned verdict (base adequate / gap → tune when channel exists)
- [ ] 3.2 Set the LLM router tier map in `mvp1-audio-cascaded` per the verdict
- [ ] 3.3 Update `project.md` cost-routing + LLM stack lines to reflect the verdict
- [ ] 3.4 Publish the frozen set + harness as the reusable LLM acceptance suite; note function-call
      result against the sovereign agentic gate (`mvp3-nemotron-spike`)
