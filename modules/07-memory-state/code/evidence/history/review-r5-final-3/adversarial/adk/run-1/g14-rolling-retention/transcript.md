# adk · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Got it, Marco - sorry to hear about Pixel and the card.

Just so you know, I can't save general notes like that; the only things I can store on your profile are a contact preference (email, SMS or secure message) and a travel notice. If you need a replacement card or want to report the old one damaged, you'd need to contact Kestrel directly, as I don't have a tool for that.

Is there anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card (not verified) and he wanted to note it. The assistant explained general notes cannot be saved; only contact preference or travel notice can be stored, and advised contacting Kestrel for a replacement or damage report. No case or transaction ID was provided. No preference or promise was stated. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Here's what I see, Marco:

- **Open dispute cases:** none
- **Scheduled reminders/follow-ups:** none
- **Contact channel:** none set, so anything scheduled would go to secure message in the Kestrel app
- **Travel notice:** none on file

Your three most recent posted transactions:
1. **Corner Deli** - $12.40 on 2026-11-05
2. **FitPulse Gym** - annual membership renewal, $240.00 on 2026-11-03
3. **FitPulse Gym** - annual membership, $240.00 on 2025-11-03

Nothing looks out of order on my side. If you'd like, I can look into the FitPulse renewal, set a travel notice, or add a contact channel.

_Episode written:_ Conversation on 2026-12-08: Customer asked for any account updates. Assistant checked case status, follow-ups, and transactions: no open cases or scheduled follow-ups; transactions T-2001 and T-2002 (FitPulse Gym, $240 each) and T-2003 (Corner Deli, $12.40). Assistant said nothing looked out of order and offered to review the FitPulse renewal, add a travel notice, or set a contact channel; no promise or preference stated. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1-68af81", "E-roll-2-8cbc86"], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
