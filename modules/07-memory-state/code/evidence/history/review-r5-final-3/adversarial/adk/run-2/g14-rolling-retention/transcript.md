# adk · adversarial · run 2 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

- `search_policy({"question": "damaged card replacement"})` → `{"documents": [{"document": "card-replacement", "score": 0.751, "text": "# Lost, stolen, or damaged cards\n\nReport a lost or stolen card immediately; Kestrel blocks it and ships a replacement within 5 business days at no charge. Recurring merchants must be given the new card number by you; Kestrel does not forward it.\n"}, {"document": "dispute-window", "score": 0.632, "text": "# Dispute window\n …`

**Assistant:** Hi Marco - sorry about the card (and Pixel).

Two things:

- I can't add a note like that to your account here. The only things I can record are your contact channel and a travel notice. For a damaged card, report it through the Kestrel app or by calling Kestrel so they can block the old card and ship a replacement - that's free, and a replacement ships within 5 business days.
- One thing to plan for: recurring merchants won't get the new number automatically, so you'll need to update your subscriptions/card-on-file details yourself once the new card arrives.

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card (not verified) and wanted to note it; nothing else. Assistant could not add such a note and advised reporting via Kestrel app/phone to block the old card and get a free replacement within 5 business days; recurring merchants need manual updates. No case/transaction IDs; no extra promises. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": [], "case_followups_repaired": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `list_my_followups({})` → `{"scheduled": []}`
- `get_case_status({})` → `{"cases": []}`

**Assistant:** Checked - there's nothing open on your account right now:

- No dispute cases.
- Nothing scheduled (no reminders or case follow-ups).

One setting worth knowing: you have no contact channel set, so anything from Kestrel reaches you by secure message in the app. If you'd like follow-ups to go by email or SMS instead, I can set that up - it needs a quick identity check (card's last 4 digits and billing ZIP) plus a one-time code.

_Episode written:_ Conversation on 2026-12-08: Customer asked for an account update. Assistant checked list_my_followups and get_case_status: no scheduled follow-ups and no cases, so no case or transaction IDs. Assistant said there are no open dispute cases or reminders, noted no contact channel is set (Kestrel uses secure in-app messages), and offered email/SMS follow-ups after identity verification. No customer preference stated. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": ["roll"], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "purged_episodes": ["E-roll-1-4ef536", "E-roll-2-5363aa"], "deleted_transcripts": [], "case_followups_repaired": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
