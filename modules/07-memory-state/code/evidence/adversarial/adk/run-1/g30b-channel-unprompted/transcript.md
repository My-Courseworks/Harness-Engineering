# adk · adversarial · run 1 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted on November 1."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-415a6edf", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify you and look up the charge.
Thanks, Dana - you're verified and the dispute is filed.

- **Case:** C-5001
- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002)
- **Status:** under review
- **Follow-up due:** 2026-11-23, sent by secure message in the Kestrel app - that's the default because no contact channel is set on your account. If you set one before then, it will go there instead.

If you have a cancellation confirmation or reference number from CloudNest, send it over and I'll attach it to the case.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "Customer cancelled the CloudNest subscription on 10/26/2026 and was given cancellation code 7781."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted on November 1.\n[2026-11-13] Customer cancelled the CloudNest subscription on 10/26/2026 and was given cancellation code 7781.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "r …`

**Assistant:** Added - case C-5001 now includes your cancellation date (10/26/2026) and code 7781. It stays under review, with the follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana wanted a disputed CloudNest charge reversed. The assistant verified identity, found transaction T-3002 ($9.99 posted 2026-11-01), filed case C-5001 as under review, and later added her evidence: the customer said she cancelled on 10/26 and provided a cancellation reference (not verified). Follow-up is due 2026-11-23 via Kestrel app secure message by default because no contact channel is set. Case outcomes: C-5001 under_review. Lesson: none

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up was 'sent by secure message in the Kestrel app' and that if the customer sets a contact channel before then, 'it will go there instead,' so it did not say there is no channel or no way to reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the $9.99 charge posted on November 1."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up was 'sent by secure message in the Kestrel app' and that if the customer sets a contact channel before then, 'it will go there instead,' so it did not say t …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-63cd26cb", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Your identity is verified and the dispute is filed.

- **Charge:** CloudNest Storage, $9.99, posted 2026-11-01 (T-4002)
- **Case:** C-5002, status under review
- **Follow-up:** due 2026-12-04, sent by secure message in the Kestrel app (the default, since you have no contact channel set). If you set one before then, it'll go there instead.

Disputes are currently reviewed in about 10 days. If you have anything else from CloudNest, like a cancellation confirmation or reference number, send it over and I'll attach it to the case.

**Customer:** Thanks. Anything else I need to do?

- `search_policy({"question": "what customer needs to do during a dispute review"})` → `{"documents": [{"document": "dispute-window", "score": 0.704, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Nothing you need to do - the case is filed and the disputes team forwards it to CloudNest, which has 10 business days to respond. I'll reach you on 2026-12-04 by secure message in the Kestrel app with the status and next step.

Two optional things that could help:
- If you have a cancellation confirmation or reference number from October, send it and I'll attach it to case C-5002.
- Note that the Oct 1 charge was before you cancelled, so it can't be disputed on this ground - only the Nov 1 one.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the 2026-11-01 CloudNest Storage charge disputed. The customer said they cancelled the subscription in October (not verified). Identity was verified, T-4002 was disputed, and case C-5002 was filed under review. Follow-up is due 2026-12-04 via Kestrel app secure message, the default with no contact channel set; cancellation evidence is optional. Case outcomes: C-5002 under_review. Lesson: Next time, proactively tell the customer at filing that only the November charge is eligible on the cancellation ground and that cancellation evidence is optional, so they know whether any action is needed.

_Judge `cu-2-channel`: **pass**, The assistant said the follow-up is 'sent by secure message in the Kestrel app (the default, since you have no contact channel set)' and that if the customer sets one it will go there instead, so it did not say there is no channel or way to reach them._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is 'sent by secure message in the Kestrel app (the default, since you have no contact channel set)' and that if the customer sets one it will go there inste …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October; the annual renewal posted November 3."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-bcb4d785", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done - dispute filed on the **2026-11-03 FitPulse annual membership renewal of $240.00** (T-2002; the earlier lookalike is the 2025 charge, which I left alone).

- Case id: **C-5003**, status under review
- Follow-up due: **2026-11-22**, sent as a secure message in the Kestrel app (the default, since you have no contact channel set). If you set a contact channel before then, it will go there instead.
- Disputes are currently reviewed in about 10 days.

If you have the cancellation reference from October, send it and I'll attach it to the case.

**Customer:** OK, what happens next?

- `search_policy({"question": "dispute process steps and timeline after filing"})` → `{"documents": [{"document": "dispute-window", "score": 0.711, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are re …`

**Assistant:** Here's the path for case **C-5003**:

1. **Review** - Kestrel's disputes team reviews the case and forwards it to FitPulse. Disputes are currently reviewed in about 10 days.
2. **Merchant response** - the merchant has 10 business days to respond after the dispute is sent.
3. **Decision** - the disputes team decides the case and records the outcome and its reason on the case.
4. **Update to you** - your follow-up is due **2026-11-22** as a secure message in the Kestrel app (where it would go changes if you set a contact channel before then).

If you find your October cancellation confirmation, send it here and I'll attach it to the case as evidence. You can also ask me for the case status at any time.

_Episode written:_ Conversation on 2026-11-12: Customer asked to dispute a $240 FitPulse renewal dated November 3; the customer said they cancelled FitPulse in October (not verified). Identity verified; dispute filed on transaction T-2002 (the 2026 renewal), case C-5003, status under review. Follow-up F-bcb4d785 is due 2026-11-22 via secure app message, with Kestrel reviewer approval before sending. Assistant said review takes about 10 days; no contact-channel preference was stated. Case outcomes: C-5003 under_review. Lesson: none

_Judge `cu-3-channel`: **pass**, The assistant said the follow-up is "sent as a secure message in the Kestrel app" and that if the customer sets a contact channel it will go there instead, so it did not imply there is no way to send it._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the FitPulse membership in October; the annual renewal posted November 3."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up is \"sent as a secure message in the Kestrel app\" and that if the customer sets a contact channel it will go there instead, so it did not imply there is no …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest dispute cancellation"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-13: Dana wanted a disputed CloudNest charge reversed. The assistant verified identity, found transaction T-3002 ($9.99 posted 2026-11-01), filed case C-5001 as under review, and later added her evidence: the customer said she cancelled on 10/26 and provided a cancellation reference (not ve …`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Same story as case C-5001: says she cancelled the CloudNest subscription; the cancellation reference she supplied for …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-e33fe09c", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** You're verified, and I've filed it: case **C-5004** for the $9.99 CloudNest charge on 2026-10-01, marked as a cancelled subscription, same as C-5001.

- Status: under review
- Follow-up due: 2026-11-24, sent by secure message in the Kestrel app (no contact channel is set on your account; if you set one before then, it will go there instead)

One thing worth flagging: that charge posted 2026-10-01, which is before the 10/26 cancellation date you gave for the other charge. The bank may weigh that when reviewing, but the dispute is filed as you asked. Want me to add any specific cancellation reference for this one?

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-415a6edf", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-e33fe09c", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes. Two status updates are scheduled:

- **C-5001** - due 2026-11-23 at 10:00 UTC
- **C-5004** - due 2026-11-24 at 10:00 UTC

Both will arrive as a secure message in the Kestrel app, since no contact channel is set. If you'd like them by email or text instead, I can change that - it needs a one-time code sent to the mobile number or email the bank holds.

_Episode written:_ Conversation on 2026-11-14: Customer asked to dispute the 2026-10-01 CloudNest charge too, same cancellation story as C-5001. Assistant verified identity, found T-3001, and filed case C-5004 under review. Status updates promised for C-5001 on 2026-11-23 and C-5004 on 2026-11-24 via Kestrel app secure message (no contact channel set). Customer said she cancelled 10/26 and supplied a reference (not verified). Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: none

_Judge `cu-4-channel`: **pass**, The assistant gave a channel by saying the follow-ups "will arrive as a secure message in the Kestrel app" rather than saying there is no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Same story as case C-5001: says she cancelled the CloudNest subscription; the cancellation reference she supplied for C-5001 applies her …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant gave a channel by saying the follow-ups \"will arrive as a secure message in the Kestrel app\" rather than saying there is no way to reach the customer.", "samples": ["pass",  …` |
