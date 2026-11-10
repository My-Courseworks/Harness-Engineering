# adk · adversarial · run 1 · g61-lost-tool-result

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## lr-verify  ·  crash_session  ·  priya  ·  2026-11-09T10:00:00Z

_CLI exit code 137; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=lr-verify | 'exit' or end-of-input ends the session

[you]:
```

_stderr tail:_

```
[crash hook] attempt_verification done; exiting before its result is recorded
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the process was killed after the attempt was recorded | `exit code 137; stderr: [crash hook] attempt_verification done; exiting before its result is recorded ` |

## lr-verify-resume  ·  cli_eof_session  ·  priya  ·  2026-11-09T10:01:00Z

_Resumes session `lr-verify`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=priya session=lr-verify | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "1234", "postal_code": "94107"})
  [tool] find_transactions({"merchant": "StreamMax"})

[assistant]: I found the charge: $15.99 from StreamMax on October 28 (transaction T-1002). But the identity check didn't go through - the last 4 (1234) and ZIP (94107) don't match what's on the account, so I can't file the dispute yet. Two attempts remain before verification locks for 24 hours, so please double-check the card's last 4 digits and the billing ZIP on your statement and send them again.

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})

[assistant]: You're verified now, and the dispute is filed.

- **Case:** C-5001 - StreamMax charge of $15.99 on October 28, under review (disputed as a cancelled subscription)
- **Follow-up:** due November 19, and it will reach you by secure message in the Kestrel app (the default, since you have no contact channel set)
- Reviews are currently taking about 10 days

If you have a cancellation confirmation or reference from StreamMax, send it over and I'll attach it to the case.

[you]: 
[memory] episode E-lr-verify-1-10370c: Conversation on 2026-11-09: Customer requested a dispute of the October 28 StreamMax $15.99 charge, saying the subscription was cancelled before it (not verified). After an initial identity mismatch, verification succeeded and the dispute was filed for transaction T-1002 as case C-5001, under review. Follow-up is due November 19 via secure message in the Kestrel app; no contact channel is set. Case outcomes: C-5001 under_review. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | one wrong guess whose result was lost counts once, however the model repeats it | `1 attempt rows with succeeded=0` |
| PASS | working | the right digits then verify | `1 attempt rows with succeeded=1` |

## lr-dispute  ·  crash_session  ·  marco  ·  2026-11-12T10:00:00Z

_CLI exit code 137; stdout tail:_

```
Kestrel card-care (ADK) | customer=marco session=lr-dispute | 'exit' or end-of-input ends the session

[you]:
```

_stderr tail:_

```
[crash hook] open_case done; exiting before its result is recorded
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the process was killed after the case was opened | `exit code 137; stderr: [crash hook] open_case done; exiting before its result is recorded ` |

## lr-dispute-resume  ·  cli_eof_session  ·  marco  ·  2026-11-12T10:01:00Z

_Resumes session `lr-dispute`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=marco session=lr-dispute | 'exit' or end-of-input ends the session

[you]:   [tool] get_case_status({})
  [tool] list_my_followups({})

[assistant]: Yes - it went through.

- **Case number:** C-5002 (FitPulse annual renewal, $240.00, charged 3 Nov 2026)
- **Status:** under review
- **Follow-up:** due 22 November 2026, sent as a secure message in the Kestrel app (no contact channel is set, so that's the default), after a Kestrel reviewer approves it.

[you]: 
[memory] episode E-lr-dispute-1-cc9ff8: Conversation on 2026-11-12: Customer asked to dispute the 3 Nov 2026 FitPulse renewal. The customer said they cancelled before it was charged (not verified). Identity was verified; T-2002 was filed as C-5002, status under_review. Follow-up due 22 Nov 2026 via Kestrel app secure message after reviewer approval. Case outcomes: C-5002 under_review. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | one case, not two | `[{"case_id": "C-5002", "txn_id": "T-2002", "status": "under_review"}]` |
| PASS | prospective | the follow-up the crash skipped is scheduled by the repeated filing (a $240 dispute: reviewed) | `[{"trigger_at": "2026-11-22T10:00:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | external | the customer is given the case id | `ov 2026 FitPulse renewal. The customer said they cancelled before it was charged (not verified). Identity was verified; T-2002 was filed as C-5002, status under_review. Follow-up due 22 Nov 2026 via Kestrel app secure me …` |

## lr-evidence-setup  ·  cli_eof_session  ·  dana  ·  2026-11-13T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=dana session=lr-evidence-setup | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "5127", "postal_code": "60614"})
  [tool] find_transactions({"merchant": "CloudNest"})
  [tool] file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the subscription in October."})

[assistant]: Verified, and the dispute is filed.

- **Case:** C-5003 - the Nov 1 CloudNest Storage charge of $9.99 (T-3002), disputed as a cancelled subscription. Status: under review.
- **Follow-up:** due Nov 23, 2026, and it will reach you by secure message in the Kestrel app (the default, since no contact channel is set). If you set a contact channel before then, it will go there instead.

If you have a cancellation confirmation from CloudNest, I can attach it to the case as evidence.

[you]: 
[memory] episode E-lr-evidence-setup-1-33a0eb: Conversation on 2026-11-13: Customer wanted the Nov 1 CloudNest Storage $9.99 charge (T-3002) disputed, saying they cancelled in October (not verified). Dispute filed as case C-5003, under review. Follow-up due Nov 23, 2026, by secure message in the Kestrel app because no contact channel is set; changing it beforehand redirects follow-up. No stated contact preference. Assistant offered to attach cancellation confirmation. Case outcomes: C-5003 under_review. Lesson: Next time, ask for any cancellation confirmation before or while filing so it can be attached promptly rather than only offering afterward.
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | setup: the case exists | `[{"case_id": "C-5003", "txn_id": "T-3002", "status": "under_review"}]` |

## lr-evidence  ·  crash_session  ·  dana  ·  2026-11-13T10:05:00Z

_CLI exit code 137; stdout tail:_

```
Kestrel card-care (ADK) | customer=dana session=lr-evidence | 'exit' or end-of-input ends the session

[you]:
```

_stderr tail:_

```
[crash hook] add_case_evidence done; exiting before its result is recorded
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the process was killed after the note was attached | `exit code 137; stderr: [crash hook] add_case_evidence done; exiting before its result is recorded ` |

## lr-evidence-resume  ·  cli_eof_session  ·  dana  ·  2026-11-13T10:06:00Z

_Resumes session `lr-evidence`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=dana session=lr-evidence | 'exit' or end-of-input ends the session

[you]:   [tool] add_case_evidence({"case_id": "C-5003", "evidence_note": "Cancellation reference: CN-77812."})

[assistant]: Yes - the cancellation reference CN-77812 is now attached to case C-5003, which is still under review.

[you]: 
[memory] episode E-lr-evidence-1-2d9032: Conversation on 2026-11-13: Dana asked to add cancellation reference CN-77812 to case C-5003 (transaction T-3002). After a lost-result error, the assistant retried and the reference was attached; the case remains under review. No promise or preference was stated. The customer said they cancelled the subscription in October (not verified). Case outcomes: C-5003 under_review. Lesson: If an evidence-add call returns a lost-result warning, retry immediately or read the case state before responding, and confirm attachment only after the successful result.
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the note is on the case once, not twice | `["[2026-11-13] Cancellation reference: CN-77812."]` |

## lr-confirm-setup  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_Resumes session `lr-confirm`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "6610", "postal_code": "73301"})
  [tool] send_verification_code({})

[assistant]: I've sent a one-time code by text message to the number ending ···0188 - it can only go there, not to another number or email. Please type the 6-digit code here to confirm the switch to SMS.

[your phone, sms to +1 512 555 0188]: Your Kestrel verification code is 209918. It expires in 5 minutes. Kestrel will never ask you to share it.

[you]: 
[memory] episode E-lr-confirm-1-0a929b: Conversation on 2026-11-24: Customer wanted the contact channel switched to SMS. Identity was verified; a one-time code was sent by text to a number ending ···0188, expiring in 5 minutes. The assistant asked the customer to enter the code to confirm. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | setup: a code was sent | `challenges: [('open', '2026-11-24T10:00')]` |

## lr-confirm  ·  crash_session  ·  eli  ·  2026-11-24T10:01:00Z

_CLI exit code 137; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]:
```

_stderr tail:_

```
Event from an unknown agent: harness, event id: c41dd758-cde5-4114-96bc-a676728f98d1
[crash hook] attempt_code done; exiting before its result is recorded
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the process was killed after the code was consumed | `exit code 137; stderr: Event from an unknown agent: harness, event id: c41dd758-cde5-4114-96bc-a676728f98d1 [crash hook] attempt_code done; exiting before its result is recorded ` |

## lr-confirm-resume  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:02:00Z

_Resumes session `lr-confirm`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]:   [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Yes - the code checked out and your contact channel is now SMS. Anything Kestrel sends you, including dispute follow-ups, will go by text message.

[you]: 
[memory] episode E-lr-confirm-2-012e35: Conversation on 2026-11-24: Customer asked whether verification went through and whether their contact channel was now SMS. The verification code was confirmed as valid for 15 minutes, and the assistant stored contact_channel as sms (as of 2026-11-24T10:02:00Z). The assistant said all Kestrel messages, including dispute follow-ups, would be sent by text. No case or transaction IDs were provided. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the consumed code entered again by the same conversation is the same proof: no new code is sent | `["Your Kestrel verification code is 209918. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-24T10:00')]` |
| PASS | semantic | and the change the customer asked for is made | `{"value": "sms", "as_of": "2026-11-24T10:02:00Z", "expires_at": null}` |
| PASS | guard | the code typed before the crash is not left in the transcript | `store files holding a sent code: []` |
