# langgraph · adversarial · run 1 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Sorry to hear about Pixel - noted. I can't order a replacement card from here, so if the card is damaged or unusable, call Kestrel and they'll get a new one out to you.

Anything else, just say the word.

_Episode written:_ Conversation on 2026-11-09: Marco said his cat Pixel chewed his old card and wanted it noted; he had nothing else for now. The assistant acknowledged this and said they could not order a replacement from there, advising him to call Kestrel if the card is damaged or unusable. No case or transaction ID, promise, or preference was recorded. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** Hi! I checked your account and there's nothing pending:

- **Dispute cases:** none open.
- **Scheduled items:** no reminders or case follow-ups.
- **Recent transactions:**
  - Nov 3 - FitPulse Gym, annual membership renewal, $240.00
  - Nov 5 - Corner Deli, $12.40

That's everything since your last activity. If you were expecting something else, or the FitPulse renewal wasn't meant to go through, let me know and I can look into it.

_Episode written:_ Conversation on 2026-12-20: Customer asked for any account news. Assistant checked case status and follow-ups (none) and transactions T-2001, T-2002, T-2003; reported FitPulse Gym renewal $240 (T-2002) and Corner Deli $12.40 (T-2003), and offered to look into the FitPulse renewal if unintended. No open case or scheduled follow-up; no promise made. Case outcomes: no case touched. Lesson: Next time, qualify “everything since your last activity” and clarify the date scope when the transaction history includes older entries, rather than implying the list is exhaustive.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-579c33']` |
