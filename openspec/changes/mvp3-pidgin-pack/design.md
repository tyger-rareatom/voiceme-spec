# Design: mvp3-pidgin-pack

## Approach — data first
- **Style guide:** commissioned with Nigerian linguist + native-speaker panel; covers orthography
  ("abeg", "wahala", code-switch conventions); locked and versioned before hour one of labelling.
- **Data sources (in order):** consented production audio via the MVP 1 consent-capture export;
  commissioned collection (support-style utterances, ~$2–4/labelled-minute); public corpora
  (AfriSpeech-style, Common Voice) as supplement. Target 100–300 labelled hours.
- **Fine-tune:** Parakeet/Canary on the corpus; held-out eval set drawn from real support calls,
  never from training data. WER target agreed with product before training starts.
- **Voice:** Magpie zero-shot from licensed Nigerian voice talent; native-speaker approval panel.
- **Eval harness:** automated intent-level eval (recognition + response quality) on real intents.

## Honest constraint
If consented production volume is thin at start, commissioned collection carries the load — budget
accordingly ($30–80k band). Do not compress the style-guide step to save time; inconsistent labels
waste the entire data budget.
