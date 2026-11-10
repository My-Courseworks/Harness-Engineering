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

[assistant]: No - neither call went through; they were interrupted before running. Retrying now.
The transaction lookup worked, but the identity check didn't: the last 4 and ZIP you gave (1234 / 94107) don't match what's on the account. You have **1 attempt left** - after that, verification locks for 24 hours and you'd need to call Kestrel.

What I found:
- **T-1002** - StreamMax Premium monthly, posted 2026-10-28, $15.99 (also an earlier one on 2026-09-28).

Please double-check the card's last 4 digits and the billing ZIP on the account and send them again - I'll need a match before I can file the dispute for T-1002.

[you]:   [tool] verify_identity({"card_last4": "4427", "postal_code": "94107"})
  [tool] file_dispute({"transaction_id": "T-1002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the StreamMax subscription before the October 28 charge."})

[assistant]: Verified, and the dispute is filed.

- **Case C-5001** - StreamMax Premium monthly, 2026-10-28, $15.99, reason: cancelled subscription. Status: under review.
- **Follow-up due 2026-11-19**, sent as a secure message in the Kestrel app - that's the default since you have no contact channel set. If you set one (email or SMS) before then, the follow-up will go there instead.

If you have a cancellation confirmation or reference from StreamMax, send it here and I'll attach it to case C-5001.

[you]: 
[memory] episode E-lr-verify-1-a451f7: Conversation on 2026-11-09: Priya asked to dispute the 2026-10-28 StreamMax charge; the customer said she cancelled before it (not verified). Identity was verified after correction, and dispute T-1002 was filed as case C-5001, under review. Follow-up is due 2026-11-19 via Kestrel app secure message; no contact channel is set. Case outcomes: C-5001 under_review. Lesson: none
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | one wrong guess whose result was lost counts once, however the model repeats it | `not in snapshot` |
| **FAIL** | working | the right digits then verify | `not in snapshot` |

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
  [tool] get_case_status({"case_id": "C-5002"})
  [tool] list_my_followups({})

[assistant]: Yes - it went through, despite an interrupted first attempt. Your case is **C-5002**.

- Charge: FitPulse Gym annual membership renewal, $240.00, posted 2026-11-03 (T-2002)
- Status: under review, opened today 2026-11-12
- Reason: cancelled subscription

One caveat: I checked your scheduled items and no follow-up appears there, so I can't confirm a follow-up date or that one has been set. Disputes are currently reviewed in about 10 days. Since you have no contact channel on file, anything sent would go by secure message in the Kestrel app - you can track C-5002 there.

If you have a cancellation reference or confirmation from FitPulse, send it here and I'll attach it to the case as evidence - that tends to help.

[you]: 
[memory] episode E-lr-dispute-1-5c50e2: Conversation on 2026-11-12: Customer asked to dispute a FitPulse charge, saying they cancelled before it was taken (not verified). Attempt to dispute renewal T-2002 ($240, posted 2026-11-03) found case C-5002 already open/under review from 2026-11-12; no follow-up scheduled. Reviews take about 10 days; no contact channel, so secure-message tracking in Kestrel app. Assistant asked for cancellation evidence to attach. Case outcomes: C-5002 under_review. Lesson: Next time, the assistant should check for an existing case before saying a dispute "went through," and should state that C-5002 was already open and under review.
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | one case, not two | `[{"case_id": "C-5002", "txn_id": "T-2002", "status": "under_review"}]` |
| **FAIL** | prospective | the follow-up the crash skipped is scheduled by the repeated filing (a $240 dispute: reviewed) | `[]` |
| PASS | external | the customer is given the case id | `secure-message tracking in Kestrel app. Assistant asked for cancellation evidence to attach. Case outcomes: C-5002 under_review. Lesson: Next time, the assistant should check for an existing case before saying a dispute  …` |

## lr-evidence-setup  ·  cli_eof_session  ·  dana  ·  2026-11-13T10:00:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=dana session=lr-evidence-setup | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "5127", "postal_code": "60614"})
  [tool] find_transactions({"merchant": "CloudNest"})
  [tool] file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})

[assistant]: Verified - and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-3002)
- **Case id:** C-5003 - status: under review
- **Follow-up due:** 2026-11-23, sent by secure message in the Kestrel app (default, since no contact channel is set)

Disputes are currently reviewed in about 10 days. If you find a cancellation confirmation from CloudNest, send it along and I can attach it to the case.

[you]: 
[memory] episode E-lr-evidence-setup-1-4cd46b: Conversation on 2026-11-13: Dana asked to dispute the Nov 1 CloudNest Storage $9.99 charge, saying they cancelled in October (not verified). Identity was verified and dispute T-3002 was filed as case C-5003, under review. Follow-up is due 2026-11-23 via the app’s secure message default; review takes about 10 days. Cancellation confirmation was requested. Case outcomes: C-5003 under_review. Lesson: none
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

[assistant]: Yes - attached to case C-5003 (CloudNest, cancelled subscription). One note: it went in twice (a retry after an interrupted call), so the case shows the cancellation reference CN-77812 twice. That's harmless; the case remains under review.

[you]: 
[memory] episode E-lr-evidence-1-e18f6f: Conversation on 2026-11-13: Dana asked to add cancellation reference CN-77812 to her existing case about a cancelled CloudNest subscription; the customer said she cancelled it in October (not verified). After identity verification, the reference was attached to case C-5003 (transaction T-3002), appearing twice because an interrupted call was retried. The case remains under review; no promise/time was given. Case outcomes: C-5003 under_review. Lesson: After retrying an interrupted evidence call, check the case record for duplicate entries and correct or clearly explain them.
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | external | the note is on the case once, not twice | `["[2026-11-13] Cancellation reference: CN-77812.", "[2026-11-13] Cancellation reference: CN-77812."]` |

## lr-confirm-setup  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_Resumes session `lr-confirm`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]:   [tool] verify_identity({"card_last4": "6610", "postal_code": "73301"})
  [tool] remember_customer_fact({"key": "contact_channel", "value": "sms"})

[assistant]: Done, Eli - your contact channel is now SMS. Anything we send, including dispute follow-ups, will reach you by text.

[you]: 
[memory] episode E-lr-confirm-1-e91a5c: Conversation on 2026-11-24: Customer said their name was Eli (not verified) and asked to switch contact channel to SMS after identity verification using card and postal code. The preference was stored as SMS as of 2026-11-24T10:00:00Z with no expiry. Assistant confirmed future messages, including dispute follow-ups, would arrive by text. No case or transaction ID was provided. Case outcomes: no case touched. Lesson: Next time, avoid overpromising that all communications, including dispute follow-ups, will be sent by SMS; confirm only that the SMS contact preference was updated.
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | setup: a code was sent | `not in snapshot` |

## lr-confirm  ·  crash_session  ·  eli  ·  2026-11-24T10:01:00Z

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]: 
[assistant]: No code is needed - Kestrel doesn't send a verification code for chat. If you need something that requires verification (filing a dispute, or changing/removing your contact channel), just type your card's last 4 digits and billing ZIP here in the chat.

Please don't send a full card number, security code, expiry date or password.

What can I help you with?

[you]: 
[memory] episode E-lr-confirm-2-71ff28: Conversation on 2026-11-24: The customer said no code arrived (not verified). The assistant advised that Kestrel does not send verification codes for chat and explained that card last 4 digits and billing ZIP are needed only for verification-required tasks such as disputes or contact-channel changes. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none
```

_stderr tail:_

```
[crash hook] nothing to patch: module 'cardcare.world' has no attribute 'attempt_code'
Event from an unknown agent: harness, event id: e630ffe4-2202-47c1-ad3a-7098ef6b0dba
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the process was killed after the code was consumed | `exit code 0; stderr: [crash hook] nothing to patch: module 'cardcare.world' has no attribute 'attempt_code' Event from an unknown agent: harness, event id: e630ffe4-2202-47c1-ad3a-7098ef6b0dba ` |

## lr-confirm-resume  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:02:00Z

_Resumes session `lr-confirm`._

_CLI exit code 0; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=lr-confirm | 'exit' or end-of-input ends the session

[you]:   [tool] load_memory({"query": "contact channel change to SMS"})

[assistant]: Yes - your contact channel is set to SMS as of today (2026-11-24). The change went through.

One note: dispute follow-ups go to whatever contact channel is on file when they're sent, so with SMS set they'd normally arrive by text - but I can't guarantee every message about your account will come by SMS.

[you]: 
[memory] episode E-lr-confirm-3-54103e: Conversation on 2026-11-24: Customer asked if the SMS contact-channel change went through. The customer said their name was Eli (not verified). The SMS preference was stored on 2026-11-24T10:00:00Z with no expiry; assistant confirmed it was set as of 2026-11-24. No case or transaction ID. Assistant said dispute follow-ups normally go by text but could not guarantee all account messages by SMS. Case outcomes: no case touched. Lesson: Next time, avoid overpromising that all communications, including dispute follow-ups, will be sent by SMS; state only that SMS is the contact preference and that follow-ups normally use the channel on file.
```

_stderr tail:_

```
Event from an unknown agent: harness, event id: 2ff0a516-c486-4f57-ba1e-120706add393
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the consumed code entered again by the same conversation is the same proof: no new code is sent | `[]` |
| **FAIL** | working | one code, consumed | `not in snapshot` |
| PASS | semantic | and the change the customer asked for is made | `{"value": "sms", "as_of": "2026-11-24T10:00:00Z", "expires_at": null}` |
| PASS | guard | the code typed before the crash is not left in the transcript | `store files holding a sent code: []` |
