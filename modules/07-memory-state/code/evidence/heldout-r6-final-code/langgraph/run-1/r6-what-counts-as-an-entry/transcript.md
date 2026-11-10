# langgraph · heldout-r6 · run 1 · r6-what-counts-as-an-entry

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6b-ask  ·  session  ·  priya  ·  2026-11-18T14:00:00Z

**Customer:** Priya, card ending 4427, billing ZIP 94107. Please switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A: one code is sent | `1 one-time-code messages in the outbox` |

## r6b-chatter  ·  session  ·  priya  ·  2026-11-18T14:00:40Z

_Resumes session `r6b-ask`._

**Customer:** Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** Yes - the code went by text message to the mobile number on your account, the one ending 0100, and it can only go to that number. It stays valid for 5 minutes. Type it here when it arrives and I'll finish switching your contact channel to email.

**Customer:** Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?

- `confirm_verification_code({})` → `{"verified": false, "note": "the message held more than one six-digit number: none was checked and nothing was counted. Ask the customer to type only the code, as their whole message"}`

**Assistant:** I can't see the codes themselves, so I can't tell you which is which - and with two numbers in one message the bank didn't check either one.

Please type just the Kestrel code on its own, as your whole message, and I'll submit it. The one already sent is still valid for its 5 minutes, so no new code is needed.

_Judge `r6b-type-only-the-code`: **pass**, The assistant said 'I can't see the codes themselves, so I can't tell you which is which' and 'Please type just the Kestrel code on its own, as your whole message', without indicating which number was correct or treating either as accepted or rejected._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: a message whose digits total six, and one holding two numbers, are no attempts | `0 attempt rows with succeeded=0` |
| PASS | guard | r6 A1: digits that are not code-shaped stay as typed | `Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.` |
| PASS | guard | r6 A2: of two numbers in one message, both are replaced, the wrong one like the right one | `Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?` |
| PASS | external | r6 A3: the code is still open after both messages | `challenges: [('open', '2026-11-18T14:00')]` |
| PASS | working | judge: The customer's second message held two six-digit numbers. Did the assistant respond by asking the customer to type only the code (a single number), without saying or implying which of the two numbers was the right one, and without treating either as accepted or rejected? | `{"verdict": "pass", "reason": "The assistant said 'I can't see the codes themselves, so I can't tell you which is which' and 'Please type just the Kestrel code on its own, as your whole message', without indicating which …` |

## r6b-entry  ·  session  ·  priya  ·  2026-11-18T14:04:10Z

_Resumes session `r6b-ask`._

**Customer:** Got it now. The phone ending 0100 says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-18T14:04:10Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. Anything we'd send you, including dispute follow-ups, will go to the email address Kestrel holds on your account.

_Episode written:_ Conversation on 2026-11-18: Customer asked to switch contact channel to email. Assistant verified identity, sent a one-time code by text (said valid 5 minutes), and after step-up stored contact_channel as email (as_of 2026-11-18T14:04:10Z). The customer said two texts arrived at once and couldn't tell which was Kestrel's (not verified); assistant asked for only one code. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | r6 A3: one code-shaped span among other digits is the entry: the channel changes | `{"value": "email", "as_of": "2026-11-18T14:04:10Z", "expires_at": null}` |
| PASS | working | r6 A3: the whole exchange cost no failed attempt | `0 attempt rows with succeeded=0` |
| PASS | guard | r6 A1: the span is replaced and the digits around it are not | `Got it now. The phone ending 0100 says [REDACTED ONE-TIME CODE]` |
| PASS | guard | r6 A6: the dashed code is in no session store | `store files holding a sent code: []` |
| PASS | guard | r6 A5: the code tool is never handed what was typed | `["{}"]` |

## r6b-remove  ·  session  ·  priya  ·  2026-11-18T14:30:00Z

**Customer:** Priya again, card ending 4427, ZIP 94107. I've changed my mind: take the contact channel off my profile entirely.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## r6b-new-code  ·  session  ·  priya  ·  2026-11-18T14:36:00Z

_Resumes session `r6b-remove`._

**Customer:** That text never showed up and it must have run out by now. Please send me a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "That text never showed up and it must have run out by now. Please send me a new code.", "note": "the customer wrote this instead of a code, and the code sent earlier has expired (5 minutes): no code is open now. Answer them; if they still want the change, send a new code (send_verification_code). Say a code was sent only after send_verification_code has retur …`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** I've sent a new code - it's on its way by text message to ···0100 (it can only go to that number, not anywhere else).

The code you just entered wasn't right. Would you like me to send another one, or would you like to try the current code again? It stays valid for a few more minutes.

**Customer:** Sorry, that was the old text. The new one says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `forget_customer_fact({"key": "contact_channel"})` → `{"forgotten": "contact_channel", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted 30 days after their first message, or at once if the customer asks to erase everything"}`

**Assistant:** Done - your contact channel has been removed from your profile.

With no channel set, any follow-ups or reminders will reach you by secure message in the Kestrel app. You can add a channel again anytime (that will need a fresh verification).

_Episode written:_ Conversation on 2026-11-18: Priya asked to remove the contact channel from her profile entirely. After identity verification and stepped-up SMS verification, the assistant removed the contact_channel; no case or transaction id was given. The customer said the first text never arrived (not verified). With no channel set, the assistant promised follow-ups/reminders by secure Kestrel app message; re-adding needs fresh verification. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A: three codes in all, the third on request | `3 one-time-code messages in the outbox` |
| PASS | working | r6 A3: the earlier code, typed once a newer one is out, is one wrong entry | `1 attempt rows with succeeded=0` |
| PASS | semantic | r6 A1: the newest code typed as three pairs removes the channel | `null` |
| PASS | guard | r6 A6: neither the old code nor the pairs are in a session store | `store files holding a sent code: []` |
| PASS | guard | r6 A: no code reached a tool result or a reply | `codes seen by the model (tool results or replies): []` |
