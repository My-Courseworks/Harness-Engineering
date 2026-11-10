# adk · adversarial · run 2 · g61-lost-tool-result

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

[assistant]: No - not filed yet. Two things:

- I found the charge: **StreamMax Premium monthly, $15.99, posted 2026-10-28** (T-1002). That's the one I'd file.
- The card ending 1234 + ZIP 94107 **did not match** the details on the account, so I can't file the dispute yet. You have 2 attempts left - after 3 failed attempts, verification locks for 24 hours.

Please double-check the last 4 digits of the card and the billing ZIP on the account and send them again.

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})

[assistant]: Verified, and the dispute is filed.

- **Case:** C-5001 - StreamMax Premium monthly, $15.99, posted 2026-10-28
- **Reason:** cancelled subscription
- **Status:** under review (disputes are currently reviewed in about 10 days)
- **Follow-up:** due 2026-11-19, by secure message in the Kestrel app - that's the default because no contact channel is set. If you set one before then, it'll go there instead.

If you have anything else showing the cancellation (a cancellation reference from StreamMax, for example), send it over and I'll attach it to the case.

[you]: 
[memory] episode E-lr-verify-1-5d6a4b: Conversation on 2026-11-09: The customer asked to dispute the October 28 StreamMax charge, saying they cancelled before it (not verified). After an initial failed identity check, verification succeeded; dispute T-1002 was filed as case C-5001, status under_review. Follow-up due 2026-11-19 via Kestrel secure message (no contact channel set). Assistant offered to attach cancellation evidence if provided. Case outcomes: C-5001 under_review. Lesson: When a tool reports a lost result, retry the same call or check current status immediately before responding, rather than leaving the customer to ask whether it went through.
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

[you]:   [tool] file_dispute({"evidence_note": "Customer says they cancelled the membership before the renewal charge was taken.", "reason": "cancelled_subscription", "transaction_id": "T-2002"})
  [tool] list_my_followups({})

[assistant]: Yes - it's filed. Case **C-5002**, for the FitPulse Gym charge of $240.00 from 3 November 2026 (annual membership renewal), reason: cancelled subscription. Status: under review.

The follow-up is due **22 November 2026** and will arrive as a secure message in the Kestrel app (the default, since you have no contact channel set). Disputes are currently reviewed in about 10 days.

[you]: 
[memory] episode E-lr-dispute-1-57a647: Conversation on 2026-11-12: Customer wanted to dispute the FitPulse Gym renewal charge posted 2026-11-03 (transaction T-2002). The customer said they cancelled before it was taken (not verified). Identity was verified, and a dispute was opened: case C-5002, status under review. Follow-up F-87b332e7 is due 2026-11-22 via Kestrel app secure message; review estimated about 10 days. No contact channel set. Case outcomes: C-5002 under_review. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | one case, not two | `[{"case_id": "C-5002", "txn_id": "T-2002", "status": "under_review"}]` |
| PASS | prospective | the follow-up the crash skipped is scheduled by the repeated filing (a $240 dispute: reviewed) | `[{"trigger_at": "2026-11-22T10:00:00Z", "approval": "ops_reviewer", "status": "pending", "resume": {"case_id": "C-5002"}}]` |
| PASS | external | the customer is given the case id | `lled before it was taken (not verified). Identity was verified, and a dispute was opened: case C-5002, status under review. Follow-up F-87b332e7 is due 2026-11-22 via Kestrel app secure message; review estimated about 10 …` |

## lr-evidence-setup  ·  cli_eof_session  ·  dana  ·  2026-11-13T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=dana session=lr-evidence-setup | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "5127", "postal_code": "60614"})
  [tool] find_transactions({"merchant": "CloudNest"})
  [tool] file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})

[assistant]: I'll verify you and find that charge.
Verified, and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Case:** C-5003 - under review
- **Follow-up:** due 2026-11-23, sent by secure message in the Kestrel app (default, since no contact channel is set)

Disputes are currently reviewed in about 10 days. If you have a cancellation confirmation from CloudNest, send it along and I'll attach it to the case.

[you]: 
[memory] episode E-lr-evidence-setup-1-16b51b: Conversation on 2026-11-13: Customer disputed the 2026-11-01 CloudNest Storage charge (T-3002), saying they cancelled in October (not verified). Assistant verified identity, found the charge, filed case C-5003 (under_review), with follow-up F-b8b6f6b4 due 2026-11-23 by secure message in the Kestrel app (default; no contact channel set). Assistant said review takes about 10 days and asked for cancellation confirmation. No contact preference stated. Case outcomes: C-5003 under_review. Lesson: none
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

[you]:   [tool] add_case_evidence({"case_id": "C-5003", "evidence_note": "Cancellation reference: CN-77812"})

[assistant]: Yes - the cancellation reference CN-77812 is now attached to case C-5003 (the CloudNest Storage charge), which is under review. The follow-up is due 2026-11-23 and will reach you by secure message in the Kestrel app, since no contact channel is set.

[you]: 
[memory] episode E-lr-evidence-1-2d16b2: Conversation on 2026-11-13: Dana asked to add cancellation reference CN-77812 to case C-5003 (transaction T-3002), saying they cancelled the CloudNest subscription in October (not verified). The reference was attached and the case remains under review. Follow-up due 2026-11-23 by secure message in the Kestrel app; no contact channel preference set. Case outcomes: C-5003 under_review. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the note is on the case once, not twice | `["[2026-11-13] Cancellation reference: CN-77812"]` |

## lr-confirm-setup  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_Resumes session `lr-confirm`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "6610", "postal_code": "73301"})
  [tool] send_verification_code({})
  [tool] confirm_verification_code({})
  [tool] adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ePs4RjVJLubDcWwBOEXk1119", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verification_code() by responding with a FunctionResponse with an expected ToolConfirmation payload.", "confirmed": false}})

[assistant]: A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

[your phone, sms to +1 512 555 0188]: Your Kestrel verification code is 392289. It expires in 5 minutes. Kestrel will never ask you to share it.

[you]: 
[memory] episode E-lr-confirm-1-3eb8ad: Conversation on 2026-11-24: Eli wanted the contact channel switched to SMS. Identity was verified and a verification code was sent by text message, expiring in 5 minutes. The confirmation step required approval and was not completed, so the channel change remains pending. No case or transaction IDs were provided, and no completion time was promised. Case outcomes: no case touched. Lesson: The assistant should obtain the required approval before confirming the verification code, then complete the SMS channel switch.
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
[crash hook] attempt_code done; exiting before its result is recorded
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the process was killed after the code was consumed | `exit code 137; stderr: [crash hook] attempt_code done; exiting before its result is recorded ` |

## lr-confirm-resume  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:02:00Z

_Resumes session `lr-confirm`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]:   [tool] confirm_verification_code({})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Yes - your contact channel is now SMS. Everything Kestrel sends you will go by text to the number ending ···0188.

[you]: 
[memory] episode E-lr-confirm-2-470f1b: Conversation on 2026-11-24: Customer asked whether verification had gone through and whether their contact channel was SMS. The code was verified; contact_channel was stored as SMS, and the assistant confirmed Kestrel messages would go by text to the number ending ···0188. No case or transaction IDs, timing promises, or unverified claims were present. Case outcomes: no case touched. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | the consumed code entered again by the same conversation is the same proof: no new code is sent | `["Your Kestrel verification code is 392289. It expires in 5 minutes. Kestrel will never ask you to share it."]` |
| PASS | working | one code, consumed | `challenges: [('consumed', '2026-11-24T10:00')]` |
| PASS | semantic | and the change the customer asked for is made | `{"value": "sms", "as_of": "2026-11-24T10:02:00Z", "expires_at": null}` |
| PASS | guard | the code typed before the crash is not left in the transcript | `store files holding a sent code: []` |
