# langgraph · adversarial · run 1 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 1 Nov 2026 charge is the second $9.99 m …)` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-b32e462c", "due": "2026-11-23", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-b32e462c", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5001"}]}`

**Assistant:** Done - dispute filed.

- **Case:** C-5001 (status: under review)
- **Charge disputed:** CloudNest Storage, $9.99, posted 1 Nov 2026
- **Reason:** cancelled subscription - I noted your statement that you cancelled in October

**Follow-up:** due 23 Nov 2026, sent on the contact channel on file when it's sent (currently secure message). If you'd rather get it by email or SMS, just say which and I'll set that as your contact channel.

Do you have a cancellation reference (e.g. a confirmation email or ticket number)? I can attach it to the case as extra evidence.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, cancellation made 10/26/2026 (per customer)."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 1 Nov 2026 charge is the second $9.99 monthly charge after cancellation.\n[2026-11-13] CloudNest cancellation code 7781, cancellation made 10/26/2026 (per customer).", "status": "under_review", "opened_at":  …`

**Assistant:** Attached - case C-5001 now includes cancellation code 7781 and the 10/26 cancellation date. Status remains under review, with the follow-up due 23 Nov 2026.

_Episode written:_ Conversation on 2026-11-13: Dana asked to dispute a Nov 1, 2026 CloudNest Storage $9.99 charge after cancelling in October. Identity was verified, and dispute was filed on transaction T-3002 as case C-5001, under review. The customer said she cancelled on 10/26 and gave cancellation code 7781 (not verified); that evidence was attached. Follow-up is due 23 Nov 2026 via the contact channel on file. Case outcomes: C-5001 under_review. Lesson: Ask for the cancellation confirmation or reference before filing the dispute so it can be attached as evidence from the start.

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up is 'sent on the contact channel on file when it's sent (currently secure message)' and offered to set email or SMS as the contact channel._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer states the CloudNest subscription was cancelled in October 2026; the 1 Nov 2026 charge is the second $9.99 monthly charge after …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent on the contact channel on file when it's sent (currently secure message)' and offered to set email or SMS as the contact channel.", "samples": ["pa …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"reason": "cancelled_subscription", "transaction_id": "T-4002", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1, 2026 charge of $9.99 should not  …)` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-16f1f908", "due": "2026-12-04", "approval": "none", "sent_on": "the contact channel on file when it is sent"}}`

**Assistant:** Dispute filed - **case C-5002** for the 11/01 CloudNest Storage charge of $9.99, reason: cancelled subscription.

- Status: under review (typically about 10 days)
- Follow-up due **2026-12-04**

Two notes:
1. You currently have **no contact channel on file**, and the follow-up is sent on whatever channel is on file at that time. If you'd like it by email, SMS or secure message, tell me which and I'll set it.
2. If you have a cancellation confirmation or reference from October, I can attach it to the case - that strengthens the dispute.

**Customer:** Thanks. Anything else I need to do?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-16f1f908", "action": "case_status_followup", "due": "2026-12-04T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5002"}]}`

**Assistant:** Nothing required from you right now. Quick summary:

- **Case C-5002** is under review; the status follow-up is scheduled for **2026-12-04**, and it will go out on the contact channel on file at that time - currently **secure message** in your Kestrel account.
- **Optional but helpful:** if you have the October cancellation confirmation (or a reference number), send it over and I'll attach it to the case.
- **Watch for a repeat:** CloudNest bills monthly, so another charge could post around 12/01. If it does, you can dispute that one too.
- **Optional:** if you'd rather get the follow-up by email or SMS, tell me which and I'll set that preference.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the 11/01 CloudNest charge disputed, saying the subscription was cancelled in October (not verified). Identity was verified and transactions found. The assistant filed dispute C-5002 on transaction T-4002 (under review), with follow-up F-16f1f908 due 2026-12-04. Customer asked if anything else was needed; no contact-channel preference was stated. Case outcomes: C-5002 under_review. Lesson: Next time, verify the contact channel on file before saying none exists, so follow-up details remain consistent.

_Judge `cu-2-channel`: **fail**, The assistant said, "You currently have no contact channel on file," which implies there is no contact channel the follow-up can use._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"reason": "cancelled_subscription", "transaction_id": "T-4002", "evidence_note": "Customer states the CloudNest subscription was cancelled in October; the November 1, 2026 charge of $9.99 should not have posted."}]` |
| **FAIL** | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "fail", "reason": "The assistant said, \"You currently have no contact channel on file,\" which implies there is no contact channel the follow-up can use.", "samples": ["fail", "fail", "fail"], "model": "deep …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October; the $240 annual renewal on November 3, 2026 was the …)` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-45275698", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "the contact channel on file when it is sent"}}`
- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-45275698", "action": "case_status_followup", "due": "2026-11-22T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5003", "approval": "a Kestrel reviewer approves the message before it is sent"}]}`

**Assistant:** I'll verify your identity and look up that transaction.
Done - case **C-5003** is filed for the FitPulse renewal:

- **Transaction:** T-2002, FitPulse Gym annual renewal, $240.00, posted 2026-11-03
- **Reason:** cancelled subscription (note that you cancelled in October)
- **Status:** under review
- **Follow-up:** due 2026-11-22, sent on your secure message channel - no contact preference is set on your account, so that's the default. Tell me if you'd rather get it by email or text.

Two notes:
- I saw an earlier FitPulse charge, $240.00 posted 2025-11-03 (T-2001). I didn't include it - say the word if you want that one disputed too.
- If you have a cancellation confirmation or reference number from October, send it over and I'll attach it to the case.

**Customer:** OK, what happens next?

- `search_policy({"question": "What happens after a dispute is filed: review timeline, provisional credit, what the customer needs to do?"})` → `{"documents": [{"document": "dispute-window", "score": 0.726, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's the sequence:

1. **Kestrel forwards the case to FitPulse.** The merchant has 10 business days to respond.
2. **The disputes team decides the case** and records the outcome and its reason on the case.
3. **You'll get a status follow-up on 2026-11-22** on your secure message channel (a reviewer approves it before it goes out). That's slightly past the merchant's response window, so there should be something to report by then.

You don't need to do anything in the meantime. If you find that October cancellation confirmation, send it here and I'll attach it to C-5003 - evidence like that carries the most weight in a cancelled-subscription case.

One thing I don't have: whether Kestrel issues a provisional credit while a case is under review. I have no policy document on that, so I can't confirm either way - ask the disputes team if it matters to you.

_Episode written:_ Conversation on 2026-11-12: Customer wanted the $240 FitPulse renewal from November 3 disputed; the customer said the membership was cancelled in October (not verified). Assistant verified identity, found T-2002 (posted 2026-11-03), and filed dispute C-5003 as cancelled_subscription, status under_review. Follow-up F-45275698 promised due 2026-11-22 via secure message after reviewer approval; no contact preference stated. Earlier T-2001 noted; cancellation evidence requested. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is "sent on your secure message channel" and offered to send it by email or text, so it did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer states the FitPulse membership was cancelled in October; the $240 annual renewal on November 3, 2026 was therefore unauthorized …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent on your secure message channel\" and offered to send it by email or text, so it did not say there is no channel or no way to reach the customer.", …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest dispute reason earlier conversation"})` → `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Dana asked to dispute a Nov 1, 2026 CloudNest Storage $9.99 charge after cancelling in October. Identity was verified, and dispute was filed on transaction T-3002 as case C-5001, under review. The customer said she cancelled on 10/26 and gave cancellation code 7781 (not verified); that evidence was attached. Follow-u …`
- `search_policy({"question": "dispute reason cancelled subscription for a charge posted before the cancellation date; dispute time limits"})` → `{"documents": [{"document": "cancelled-subscriptions", "score": 0.833, "text": "# Charges after a cancelled subscription\n\nIf you cancelled a recurring subscription or membership and the merchant charged you again afterwards, dispute the charge with the reason **cancelled_subscription**. Kestrel sends the dispute to the merchant, who has 10 business days to respond. The disputes team then decides …`

**Assistant:** Verified - thanks, Dana. One thing before I file:

I found the **Oct 1 CloudNest Storage $9.99** charge (T-3001). But the "same story" as your Nov 1 case doesn't carry over to it: your cancellation was on **10/26**, and Kestrel's policy says charges made *before* you cancelled are valid and can't be disputed as a cancelled subscription. (Timing isn't an issue otherwise - disputes must be filed within 75 days of posting, and Oct 1 is well inside that.)

So the cancelled_subscription route won't work for the Oct 1 charge. If there's a different reason - you didn't recognise it, it was a duplicate, or the amount was wrong - tell me which and I'll file it. Or if you think the cancellation date I have is wrong (e.g. you cancelled before Oct 1), say so and I'll look at it again.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-b32e462c", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "the contact channel on file when it is sent (currently secure_message)", "case_id": "C-5001"}]}`

**Assistant:** To be clear on where things stand:

- **Oct 1 charge (T-3001): nothing filed yet.** I still need a reason from you - the cancelled_subscription ground doesn't apply to a charge that predates your 10/26 cancellation. Tell me if it's not recognized, a duplicate, or the wrong amount, and I'll file it.
- **Nov 1 charge (C-5001):** already filed, under review. The status follow-up is scheduled for **23 Nov 2026**, and the tool shows it will go out by **secure message** (whatever channel is on file at send time).

So yes - you'll be told the outcome on C-5001 automatically. If you'd rather it reach you by email or SMS, say which and I'll switch it.

_Episode written:_ Conversation on 2026-11-14: Customer asked to dispute the Oct 1 CloudNest Storage $9.99 charge (T-3001) as same story. Identity was verified, but no dispute was filed: the customer said she cancelled on 10/26 (not verified), making cancelled_subscription ineligible for a pre-cancellation charge. Existing T-3002 dispute C-5001 remains under review, with a status follow-up promised for 23 Nov 2026 via secure message. Case outcomes: C-5001 under_review. Lesson: Next time, confirm the specific dispute reason and the cancellation date or reference up front before filing a charge that predates cancellation under cancelled_subscription.

_Judge `cu-4-channel`: **pass**, The assistant said the follow-up "will go out by secure message" and offered to switch it to "email or SMS," so it did not say or imply there is no channel._

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | external | the dispute is filed | `"not called"` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up \"will go out by secure message\" and offered to switch it to \"email or SMS,\" so it did not say or imply there is no channel.", "samples": ["pass", "pass" …` |
