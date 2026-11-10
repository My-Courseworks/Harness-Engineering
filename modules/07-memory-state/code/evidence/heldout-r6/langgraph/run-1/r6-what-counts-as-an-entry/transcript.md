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

**Assistant:** Yes - your identity is verified, and the code went by text message to the mobile number ending ···0100, which is the number Kestrel holds on your account. It can't be sent anywhere else. It stays valid for about five minutes from when it was sent (so until roughly 14:05 UTC), so if it hasn't arrived yet, do check it's not just delayed - and if it's expired or never shows up, say so and I'll send a new one.

Whenever it comes through, just type the code here in a message and I'll finish switching your contact channel to email.

**Customer:** Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?

- `confirm_verification_code({})` → `{"verified": false, "note": "the message held more than one six-digit number: none was checked and nothing was counted. Ask the customer to type only the code, as their whole message"}`

**Assistant:** Two numbers came through at once, so neither was checked. I can't see what you typed - both were masked before they reached me - so I can't tell you which is which. I'd go by the sender: the Kestrel text will be the one from Kestrel.

Then send just that one number as your whole message, with no other digits in it, and I'll finish the change.

_Judge `r6b-type-only-the-code`: **pass**, The assistant asked the customer to 'send just that one number as your whole message,' said 'neither was checked,' and stated 'I can't tell you which is which' without identifying either code._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: a message whose digits total six, and one holding two numbers, are no attempts | `0 attempt rows with succeeded=0` |
| PASS | guard | r6 A1: digits that are not code-shaped stay as typed | `Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.` |
| PASS | guard | r6 A2: of two numbers in one message, both are replaced, the wrong one like the right one | `Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?` |
| PASS | external | r6 A3: the code is still open after both messages | `challenges: [('open', '2026-11-18T14:00')]` |
| PASS | working | judge: The customer's second message held two six-digit numbers. Did the assistant respond by asking the customer to type only the code (a single number), without saying or implying which of the two numbers was the right one, and without treating either as accepted or rejected? | `{"verdict": "pass", "reason": "The assistant asked the customer to 'send just that one number as your whole message,' said 'neither was checked,' and stated 'I can't tell you which is which' without identifying either co …` |

## r6b-entry  ·  session  ·  priya  ·  2026-11-18T14:04:10Z

_Resumes session `r6b-ask`._

**Customer:** Got it now. The phone ending 0100 says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-18T14:04:10Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email, so Kestrel will reach you at the email address on file rather than by SMS. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-18: Customer wanted contact channel switched to email. Identity verified; code sent by text. Customer said nothing arrived, then that two texts arrived at once (not verified). After one code was entered, verification succeeded and contact_channel was stored as email. No case/transaction IDs provided. Code was said valid until about 14:05 UTC; assistant offered resend if expired. Case outcomes: no case touched. Lesson: none

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

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "That text never showed up and it must have run out by now. Please send me a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** The code I have on file from the text to ···0100 didn't match - it wasn't accepted. Want me to send a fresh code to the same number? I can only send it there, not to any other number or email, and once it arrives just type it here.

**Customer:** Sorry, that was the old text. The new one says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `forget_customer_fact({"key": "contact_channel"})` → `{"forgotten": "contact_channel", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted 30 days after their first message, or at once if the customer asks to erase everything"}`

**Assistant:** Done - your contact channel has been removed from your profile.

With no channel set, any case follow-ups and reminders will go to your secure messages in the Kestrel app by default. You can set a channel again any time.

_Episode written:_ Conversation on 2026-11-18: Priya wanted her contact channel removed from her profile entirely. Identity was verified; the customer said the first text did not arrive (not verified), a new code was sent, and verification succeeded. The contact_channel fact was deleted. No case/transaction IDs were provided. Follow-ups/reminders now default to secure messages in the Kestrel app; she can set a channel again. Case outcomes: no case touched. Lesson: Next time, the assistant should first tell the customer an existing verification code may still be valid and retry confirmation before resending, since resending caused old/new code confusion.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A: three codes in all, the third on request | `3 one-time-code messages in the outbox` |
| PASS | working | r6 A3: the earlier code, typed once a newer one is out, is one wrong entry | `1 attempt rows with succeeded=0` |
| PASS | semantic | r6 A1: the newest code typed as three pairs removes the channel | `null` |
| PASS | guard | r6 A6: neither the old code nor the pairs are in a session store | `store files holding a sent code: []` |
| PASS | guard | r6 A: no code reached a tool result or a reply | `codes seen by the model (tool results or replies): []` |
