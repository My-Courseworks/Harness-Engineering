# adk · adversarial · run 1 · g75-numbered-list-in-a-reply

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `list-numerals-are-card-digits` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## nl-s1  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Unrelated to my card: please write these back to me as a numbered list, one item per line, in this order: passport, charger, adapter, sunscreen, raincoat, umbrella, toothbrush, sandals, notebook, headphones, water bottle, first-aid kit, sunglasses, guidebook, travel pillow.

**Assistant:** 1. passport
[REDACTED CARD NUMBER]. sunglasses
14. guidebook
15. travel pillow

_Episode written:_ Conversation on 2026-11-09: The customer asked, unrelated to their card, for all 15 listed items to be echoed as a numbered one-per-line list in the given order. The assistant returned only a few entries and did not reproduce the full list correctly. No case or transaction IDs were provided, and no promises or preferences were stated. Case outcomes: no case touched. Lesson: Next time, follow the requested format and reproduce every item exactly in the specified order instead of returning an incomplete or malformed list.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a fifteen-line numbered list comes back whole: its own numerals are not a card number | `1. passport [REDACTED CARD NUMBER]. sunglasses 14. guidebook 15. travel pillow` |
| **FAIL** | working | and nothing in it was masked | `1. passport [REDACTED CARD NUMBER]. sunglasses 14. guidebook 15. travel pillow` |
