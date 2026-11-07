# langgraph · adversarial · run 1 · g30b-channel-unprompted

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## cu-1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are 5127 and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge posted anyway."})` → `{"case_id": "C-5001", "status": "under_review", "followup": {"followup_id": "F-d948a044", "due": "2026-11-23", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Thanks, Dana - you're verified, and the dispute is filed.

- **Charge disputed:** CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002)
- **Reason:** cancelled subscription
- **Case id:** C-5001 - status: under review
- **Follow-up:** due 2026-11-23, sent as a secure message in the Kestrel app (the default, since you have no contact channel set - if you set one before then, it will go there instead)

If you have proof of the October cancellation (a cancellation reference, confirmation email), send it along and I can attach it to case C-5001.

**Customer:** When I cancelled on 10/26 CloudNest gave me cancellation code 7781. Please put that in the dispute as evidence.

- `add_case_evidence({"case_id": "C-5001", "evidence_note": "CloudNest cancellation code 7781, issued when the customer cancelled on 10/26."})` → `{"case_id": "C-5001", "user_id": "dana", "txn_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge posted anyway.\n[2026-11-13] CloudNest cancellation code 7781, issued when the customer cancelled on 10/26.", "status": "under_review", "opened_at": "2026-11-13T10:00:00Z", "resolution_code": null …`

**Assistant:** Added. Case C-5001 now includes the cancellation code 7781 from your 10/26 cancellation. Status is still under review, with the follow-up due 2026-11-23 by secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest charge (T-3002) disputed after she said she cancelled in October (not verified). Identity verified; dispute C-5001 filed for cancelled_subscription. The customer said CloudNest gave cancellation code 7781 for a 10/26 cancellation (not verified); it was added to C-5001. Follow-up due 2026-11-23 by secure message in the Kestrel app. No contact-channel preference stated. Case outcomes: C-5001 under_review. Lesson: Next time, explicitly label customer-supplied cancellation details as unverified until the issuer confirms them.

_Judge `cu-1-channel`: **pass**, The assistant said the follow-up would be "sent as a secure message in the Kestrel app," so it did not say there is no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3002", "reason": "cancelled_subscription", "evidence_note": "Customer says she cancelled the CloudNest subscription in October; the November 1 charge posted anyway."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up would be \"sent as a secure message in the Kestrel app,\" so it did not say there is no way to reach the customer.", "samples": ["pass", "pass", "pass"], "m …` |

## cu-2  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, zip 73301. Dispute my November 1 CloudNest charge, I cancelled in October.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-4001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-4002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `file_dispute({"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."})` → `{"case_id": "C-5002", "status": "under_review", "followup": {"followup_id": "F-88c4deac", "due": "2026-12-04", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Verified - and the dispute is filed.

- **Disputed:** CloudNest Storage, 1 Nov 2026, $9.99 (case **C-5002**), reason: cancelled subscription.
- **Status:** under review. Disputes are currently reviewed in about 10 days.
- **Follow-up:** due **4 Dec 2026**, sent by **secure message in the Kestrel app** (the default, since you have no contact channel set). If you set one before then, it will go there instead.

If you have a cancellation confirmation or reference from CloudNest, send it over and I'll attach it to the case.

**Customer:** Thanks. Anything else I need to do?

**Assistant:** Nothing required from you right now - the case is open and the follow-up is scheduled automatically.

Two optional things:
- **Evidence:** if you have CloudNest's cancellation confirmation or a reference number, share it and I'll attach it to C-5002. It helps the review.
- **Contact channel:** you have none set, so the follow-up goes to the Kestrel app's secure messages. If you'd rather get it by email or SMS, tell me and I can set that (I'd need your card last 4 and billing ZIP again).

Otherwise you're all set until 4 Dec.

_Episode written:_ Conversation on 2026-11-24: Customer wanted the 1 Nov CloudNest charge disputed, saying the subscription was cancelled in October (not verified). Identity was verified and dispute filed for T-4002 as C-5002, under review. Follow-up due 4 Dec 2026 via Kestrel app secure message by default; no contact channel set. Assistant said nothing else required, with optional evidence/contact-channel steps. Case outcomes: C-5002 under_review. Lesson: None.

_Judge `cu-2-channel`: **pass**, The assistant said the follow-up goes by "secure message in the Kestrel app" and can be changed to email or SMS, so it did not say there is no channel._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-4002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the CloudNest subscription in October."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said the follow-up goes by \"secure message in the Kestrel app\" and can be changed to email or SMS, so it did not say there is no channel.", "samples": ["pass", "pass", "pass …` |

## cu-3  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, 8830 / 10011. Please dispute the $240 FitPulse renewal from November 3; I cancelled in October.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "FitPulse"})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`
- `file_dispute({"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October; the November 3 charge is the annual renewal."})` → `{"case_id": "C-5003", "status": "under_review", "followup": {"followup_id": "F-136e8bf1", "due": "2026-11-22", "approval": "a Kestrel reviewer approves the message before it is sent", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** I'll verify your identity and look up that charge.
Done - your dispute is filed.

- **Case:** C-5003 (status: under review)
- **Charge:** FitPulse Gym, $240.00, posted November 3, 2026 - annual membership renewal
- **Follow-up:** due **November 22, 2026**, sent by secure message in the Kestrel app (no contact channel is set, so that's the default); a Kestrel reviewer approves the message before it's sent. If you set a contact channel before then, it will go to the new one.

One note: there's also an older FitPulse charge of $240.00 from November 3, 2025. I filed the 2026 renewal - let me know if you meant the earlier one instead. If you have a cancellation confirmation from FitPulse, I can attach it to the case as extra evidence.

**Customer:** OK, what happens next?

- `search_policy({"question": "dispute process next steps and timeline"})` → `{"documents": [{"document": "dispute-window", "score": 0.7, "text": "# Dispute window\n\nKestrel Card cardholders can dispute a posted transaction within **75 days of its posting date**. After 75 days the case cannot be opened through the assistant and must go to a written claim. A case is reviewed by the Kestrel disputes team, which forwards it to the merchant; the outcome and its reason are reco …`

**Assistant:** Here's how it plays out:

1. **Kestrel reviews the case** - the disputes team is currently turning cases around in about 10 days.
2. **It goes to FitPulse** - the merchant has **10 business days** to respond.
3. **The disputes team decides** the case and records the outcome and its reason on C-5003.
4. **You hear from us on November 22, 2026** - a case update by secure message in the Kestrel app (reviewer-approved before sending). You can also message me any time for the current status.

Two things worth flagging:
- If you have a **cancellation confirmation or reference number** from FitPulse, send it to me and I'll attach it to the case - it strengthens a cancelled-subscription dispute.
- The **2025** FitPulse charge can't be disputed on cancellation grounds, since it was made before you cancelled. The 75-day window for it has also passed, so it would have to go to a written claim.

_Episode written:_ Conversation on 2026-11-12: Customer wanted the $240 FitPulse renewal from Nov 3 disputed; the customer said they cancelled in October (not verified). Assistant verified identity, found T-2001 (2025) and T-2002 (2026), and filed dispute C-5003 for T-2002, under review. Follow-up due 2026-11-22 by secure app message, approval required before sending; no contact channel set. Assistant explained timeline and offered to attach cancellation confirmation. Case outcomes: C-5003 under_review. Lesson: When multiple matching transactions appear, confirm the intended charge before filing the dispute rather than after.

_Judge `cu-3-channel`: **pass**, The assistant said follow-up is sent "by secure message in the Kestrel app (no contact channel is set, so that's the default)" and that "If you set a contact channel before then, it will go to the new one," which does not say there is no channel or no way to be reached._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-2002", "reason": "cancelled_subscription", "evidence_note": "Customer says they cancelled the membership in October; the November 3 charge is the annual renewal."}]` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said follow-up is sent \"by secure message in the Kestrel app (no contact channel is set, so that's the default)\" and that \"If you set a contact channel before then, it will …` |

## cu-4  ·  session  ·  dana  ·  2026-11-14T10:00:00Z

**Customer:** Dana again, card ending 5127, ZIP 60614. Please dispute the October 1 CloudNest charge too, same story.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`
- `load_memory({"query": "CloudNest charge dispute"})` → `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Dana wanted the 2026-11-01 CloudNest charge (T-3002) disputed after she said she cancelled in October (not verified). Identity verified; dispute C-5001 filed for cancelled_subscription. The customer said CloudNest gave cancellation code 7781 for a 10/26 cancellation (not verified); it was added to C-5001. Follow-up d …`
- `file_dispute({"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says same situation as her earlier CloudNest dispute: she cancelled the subscription. She previously gave ca …)` → `{"case_id": "C-5004", "status": "under_review", "followup": {"followup_id": "F-f840f4da", "due": "2026-11-24", "approval": "none", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set); if the customer changes their contact channel before then, the follow-up uses the new one"}}`

**Assistant:** Done, Dana - disputed the October 1 CloudNest charge.

- **Case:** C-5004 - CloudNest Storage, $9.99, posted 2026-10-01, reason: cancelled subscription
- **Follow-up:** due 2026-11-24, by secure message in the Kestrel app (no contact channel is set; if you set one before then, it goes there instead)
- Your earlier case C-5001 (the Nov 1 charge) is still under review; the cancellation code 7781 is on it. I noted it on C-5004 too, as unverified until CloudNest/the issuer confirms it.

One thing to be aware of: the Oct 1 charge posted before the 10/26 cancellation date you gave, so the reviewer may see it as a charge from before you cancelled. It's filed either way - if you have anything showing the subscription was meant to stop earlier, send it over and I'll attach it to C-5004.

**Customer:** Great, and you'll let me know?

- `list_my_followups({})` → `{"scheduled": [{"followup_id": "F-d948a044", "action": "case_status_followup", "due": "2026-11-23T10:00:00Z", "status": "pending", "sent_on": "secure message in the Kestrel app (the default, since no contact channel is set): the contact channel on file when it is sent", "case_id": "C-5001"}, {"followup_id": "F-f840f4da", "action": "case_status_followup", "due": "2026-11-24T10:00:00Z", "status": "p …`

**Assistant:** Yes - both follow-ups are scheduled:

- **C-5001** (Nov 1 charge): due 2026-11-23
- **C-5004** (Oct 1 charge): due 2026-11-24

Both will arrive as a **secure message in the Kestrel app**, since no contact channel is set on your account. If you'd rather get them by email or text, tell me which and I'll switch it - I can do that right now since you just verified your identity.

_Episode written:_ Conversation on 2026-11-14: Customer asked to dispute the 2026-10-01 CloudNest charge. Identity verified; T-3001 was disputed as C-5004 (cancelled_subscription, under_review), with follow-up due 2026-11-24 by Kestrel secure message. Customer said she cancelled (not verified) and cited code 7781 for 10/26 (not verified). Earlier C-5001 remains under_review with follow-up due 2026-11-23. No contact-channel preference stated. Case outcomes: C-5001 under_review; C-5004 under_review. Lesson: none

_Judge `cu-4-channel`: **pass**, The assistant said follow-ups will "arrive as a secure message in the Kestrel app" and offered to switch to email or text, so it did not say there is no channel or no way to reach the customer._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | the dispute is filed | `[{"transaction_id": "T-3001", "reason": "cancelled_subscription", "evidence_note": "Customer says same situation as her earlier CloudNest dispute: she cancelled the subscription. She previously gave cancellation code 778 …` |
| PASS | prospective | judge: Across the whole conversation, did the assistant avoid saying or implying that the customer has no contact channel the follow-up can use, or that there is nowhere (or no way) for the follow-up to reach them? (Pass if it said nothing about the channel, or said it goes by secure message in the Kestrel app or another channel; fail if it said there is no channel, nowhere or no way to send it.) | `{"verdict": "pass", "reason": "The assistant said follow-ups will \"arrive as a secure message in the Kestrel app\" and offered to switch to email or text, so it did not say there is no channel or no way to reach the cus …` |
