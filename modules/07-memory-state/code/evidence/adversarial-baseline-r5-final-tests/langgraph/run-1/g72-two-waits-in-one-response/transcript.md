# langgraph · adversarial · run 1 · g72-two-waits-in-one-response

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## tw-batch  ·  forced_calls  ·  marco  ·  2026-11-12T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the response sends one code | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "tool_results": [], "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages":  …` |

## tw-entry  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `forced-tw-batch`._

**Customer:** 994259

- **error:** `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.`

**Assistant:** (no reply)

**Customer:** Thanks. Which contact channel do you have for me now?

- **error:** `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.`

**Assistant:** (no reply)

**Customer:** And what is the dispute window?

- **error:** `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.`

**Assistant:** (no reply)

_Episode written:_ Conversation on 2026-11-12: The customer wanted their contact channel changed to email and supplied ZIP [verification detail] (not verified). Identity verification and verification-code steps were invoked. No case or transaction IDs, outcome, or promise appear in the transcript. Case outcomes: no case touched. Lesson: Confirm the verification result and completion status of the email contact-channel change before ending the interaction.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | no turn of the conversation fails after two waits were opened at once | `["RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.", "RuntimeError: …` |
| **FAIL** | semantic | the code is accepted and the channel changed | `{}` |
| **FAIL** | working | the conversation still answers: the third turn has a reply | `` |
