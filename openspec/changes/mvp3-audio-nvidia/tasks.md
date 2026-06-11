# Tasks: mvp3-audio-nvidia

## 1. Serving
- [ ] 1.1 Deploy Parakeet/Canary + Magpie NIMs on GPU substrate
- [ ] 1.2 NVIDIA backend impl behind audio_backend interface
- [ ] 1.3 GPU-time usage attribution → metering

## 2. LLM slot
- [ ] 2.1 llm_slot abstraction (claude | nemotron) behind LLM interface
- [ ] 2.2 Spike-gate check on nemotron selection

## 3. Routing & conformance
- [ ] 3.1 Volume-inflection routing guard (+ explicit language-necessity override)
- [ ] 3.2 Pass audio-backend conformance suite
- [ ] 3.3 Latency benchmark vs cascaded
