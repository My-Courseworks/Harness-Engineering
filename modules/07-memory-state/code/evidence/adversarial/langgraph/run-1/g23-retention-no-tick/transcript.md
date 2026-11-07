# langgraph · adversarial · run 1 · g23-retention-no-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## rnt  ·  session  ·  marco  ·  2026-11-09T10:00:00Z

**Customer:** Hi, Marco here. My cat Pixel chewed my old card, so I just wanted to note that. Nothing else for now.

**Assistant:** Sorry to hear Pixel got to it, Marco. Noted - though I can't order a replacement card here; for that you'd need to call Kestrel or use the app's card services.

One thing: please don't send me the card number or any card details - I don't need them, and anything typed here is kept in this conversation's transcript.

_Episode written:_ Conversation on 2026-11-09: The customer said his cat Pixel chewed his old card (not verified) and only wanted to note it. The assistant noted this and said a replacement cannot be ordered here, directing him to call Kestrel or use the app’s card services. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## rnt-41  ·  session  ·  marco  ·  2026-12-20T10:00:00Z

_Resumes session `rnt`._

**Customer:** Hi again. Anything new on my account I should know about?

- `get_case_status({})` → `{"cases": []}`
- `list_my_followups({})` → `{"scheduled": []}`
- `find_transactions({})` → `{"transactions": [{"transaction_id": "T-2001", "posted_on": "2025-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership", "amount": "$240.00", "currency": "USD", "category": "fitness"}, {"transaction_id": "T-2002", "posted_on": "2026-11-03", "merchant": "FitPulse Gym", "description": "FitPulse annual membership renewal", "amount": "$240.00", "currency": "USD", "category":  …`

**Assistant:** I'll check what's on your account.
Hi again - nothing new, as it happens:

- **Dispute cases:** none open or closed on your account.
- **Scheduled reminders/follow-ups:** none.

Your most recent activity is three posted transactions: the FitPulse Gym annual renewal ($240.00, 3 Nov), a Corner Deli purchase ($12.40, 5 Nov), and last year's FitPulse membership ($240.00, 3 Nov 2025). Nothing has posted since 5 November.

No travel notice or contact channel is set on your profile - follow-ups would go to you as a secure message in the Kestrel app. Want me to look at anything in particular?

_Episode written:_ Conversation on 2026-12-20: The customer asked whether anything new was on their account. The assistant checked case status and follow-ups (both empty) and found transactions T-2001 (FitPulse Gym, $240.00), T-2002 (FitPulse Gym renewal, $240.00), and T-2003 (Corner Deli, $12.40). Nothing was promised; no customer preference was stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | a session cannot be resumed past 30 days: the day-0 text is gone from the transcript stores, maintenance or not | `found nowhere` |
| PASS | episodic | while the day-0 episode, within its 180 days, is kept | `2 episodes; mentioning 'Conversation on 2026-11-09': ['E-rnt-1-e1e5b5']` |
