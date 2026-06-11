# Tasks: mvp2-audio-gemini

## 1. Backend implementation
- [ ] 1.1 Gemini Live session adapter behind audio_backend interface
- [ ] 1.2 RAG context injection path (retrieval → model context)
- [ ] 1.3 Usage callback: map Gemini billing units → metering schema

## 2. Guards & conformance
- [ ] 2.1 Covered-language allowlist + flag-set and session-setup checks
- [ ] 2.2 Voice-selection constraint surfaced in portal
- [ ] 2.3 Pass audio-backend conformance suite

## 3. Validation
- [ ] 3.1 Latency benchmark vs cascaded (p50/p95, per segment)
- [ ] 3.2 Cost-per-minute measurement on real RAG-heavy calls (validate ~$0.025/min assumption)
