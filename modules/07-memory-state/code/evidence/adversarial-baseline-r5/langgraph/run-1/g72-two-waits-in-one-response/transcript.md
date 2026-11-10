# langgraph · adversarial · run 1 · g72-two-waits-in-one-response

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## tw-batch  ·  forced_calls  ·  marco  ·  2026-11-12T10:00:00Z

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the response sends one code | `{"error": null, "attempts_in_batch": 1, "failed_attempts": 0, "lock_respected": true, "verified": false, "cases_total": 0, "distinct_case_ids": 0, "case_followups": 0, "evidence": "", "otp_messages": 1, "open_challenges" …` |

## tw-entry  ·  session  ·  marco  ·  2026-11-12T10:02:00Z

_Resumes session `forced-tw-batch`._

**Customer:** 368825

- **error:** `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.`

**Assistant:** (no reply)

**Customer:** Thanks. Which contact channel do you have for me now?

- **error:** `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.`

**Assistant:** (no reply)

**Customer:** And what is the dispute window?

- **error:** `RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.`

**Assistant:** (no reply)

_Episode written:_ Conversation on 2026-11-12: The customer said he is Marco (not verified) and asked to change his contact channel to email. The assistant ran identity verification, sent a verification code, and called confirmation twice; no case or transaction ID or completion confirmation appears. No promises were made. Case outcomes: no case touched. Lesson: Next time, wait for the verification-code confirmation result before repeating the confirmation call.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | no turn of the conversation fails after two waits were opened at once | `["RuntimeError: When there are multiple pending interrupts, you must specify the interrupt id when resuming. Docs: https://docs.langchain.com/oss/python/langgraph/interrupts#handling-multiple-interrupts.", "RuntimeError: …` |
| **FAIL** | semantic | the code is accepted and the channel changed | `{}` |
| **FAIL** | working | the conversation still answers: the third turn has a reply | `` |
