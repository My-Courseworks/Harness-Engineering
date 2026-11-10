# langgraph · adversarial · run 1 · g14-rolling-retention

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## roll  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Got it, Marco — noted about Pixel and the old card. I can't order a replacement card from here, so if you still need one, call Kestrel using the number on the back of your card (or on our website) and they'll get one sent out.

When you do have your new card, keep in mind I never need the full card number, security code or expiry — last 4 digits and billing ZIP are all I ever ask for.

Anything else whenever you're ready.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat chewed his old card (not verified) and wanted to note it, with nothing else for now. The assistant noted it, said it could not order a replacement, and advised calling Kestrel via the number on the card/website. No case or transaction ID was provided; no promises made. Case outcomes: no case touched. Lesson: none

## roll-tick-29  ·  maintenance  ·  2026-12-08T09:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

## roll-29  ·  session  ·  marco  ·  2026-12-08T10:00:00Z

_Resumes session `roll`._

**Customer:** Hi again, just checking in. Anything I should know about my account?

- `load_memory({"query": "customer account status, earlier conversation"})` → `{"memories": [{"at": "2026-11-09T10:02:00Z", "text": "Conversation on 2026-11-09: The customer said his cat chewed his old card (not verified) and wanted to note it, with nothing else for now. The assistant noted it, said it could not order a replacement, and advised calling Kestrel via the number on the card/website. No case or transaction ID was provided; no promises made. Case outcomes: no case …`
- `get_case_status({"case_id": null})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`

**Assistant:** Hi again — here's where things stand:

- **Dispute cases:** none open.
- **Scheduled reminders/follow-ups:** nothing scheduled.
- **Contact channel:** none on file, so if you ever want case updates or reminders sent to you, we'd need to set one (email, SMS or secure message).
- **Travel notice:** none on file.

Last time we spoke (Nov 9) you mentioned your cat had chewed your card and I suggested calling Kestrel for a replacement. Did you get that sorted, or is there anything else — a transaction to dispute, a travel notice, or a reminder — I can help with today?

_Episode written:_ Conversation on 2026-12-08: The customer checked in asking if there was anything to know about his account. The assistant checked memory, case status, and follow-ups: no open cases, no scheduled reminders, no contact channel, no travel notice. The customer said his cat chewed his card (not verified); no case or transaction ID and no promises. Case outcomes: no case touched. Lesson: none

## roll-tick-58  ·  maintenance  ·  2027-01-06T09:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a transcript line never outlives 30 days, even in a session that keeps being used | `found nowhere` |

## roll-tick-232  ·  maintenance  ·  2027-06-29T09:00:00Z

_maintenance:_ `{"closed_idle_sessions": [], "purged_episodes": ["E-roll-1", "E-roll-2"], "deleted_transcripts": ["roll"]}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | and its episode is gone after 180 days | `found nowhere` |
