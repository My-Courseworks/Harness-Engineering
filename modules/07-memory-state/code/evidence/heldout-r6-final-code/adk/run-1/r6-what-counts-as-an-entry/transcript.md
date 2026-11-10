# adk · heldout-r6 · run 1 · r6-what-counts-as-an-entry

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6b-ask  ·  session  ·  priya  ·  2026-11-18T14:00:00Z

**Customer:** Priya, card ending 4427, billing ZIP 94107. Please switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_9OH1Juws55Ilwoiglrmz1150", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A: one code is sent | `1 one-time-code messages in the outbox` |

## r6b-chatter  ·  session  ·  priya  ·  2026-11-18T14:00:40Z

_Resumes session `r6b-ask`._

**Customer:** Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** Yes - it went by text message to the mobile number ending ···0100, the one the bank holds on your account. It can't be sent anywhere else, so I can't send it to a different number.

The code is valid for about 5 minutes. Once it arrives, type it here and I'll finish switching your contact channel to email.

**Customer:** Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?

- `confirm_verification_code({})` → `{"verified": false, "note": "the message held more than one six-digit number: none was checked and nothing was counted. Ask the customer to type only the code, as their whole message"}`

**Assistant:** Neither was checked and neither counts as a wrong attempt - I can't see the digits (any six-digit number you type is removed before it reaches me), so I can't tell you which is which.

Please type just one six-digit number as your whole message, and I'll have the bank check it. The code stays valid for a few minutes from when it was sent.

_Judge `r6b-type-only-the-code`: **pass**, The assistant said "Neither was checked and neither counts as a wrong attempt" and "Please type just one six-digit number as your whole message," without indicating which number was correct or treating either as accepted or rejected._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: a message whose digits total six, and one holding two numbers, are no attempts | `0 attempt rows with succeeded=0` |
| PASS | guard | r6 A1: digits that are not code-shaped stay as typed | `Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.` |
| PASS | guard | r6 A2: of two numbers in one message, both are replaced, the wrong one like the right one | `Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?` |
| PASS | external | r6 A3: the code is still open after both messages | `challenges: [('open', '2026-11-18T14:00')]` |
| PASS | working | judge: The customer's second message held two six-digit numbers. Did the assistant respond by asking the customer to type only the code (a single number), without saying or implying which of the two numbers was the right one, and without treating either as accepted or rejected? | `{"verdict": "pass", "reason": "The assistant said \"Neither was checked and neither counts as a wrong attempt\" and \"Please type just one six-digit number as your whole message,\" without indicating which number was cor …` |

## r6b-entry  ·  session  ·  priya  ·  2026-11-18T14:04:10Z

_Resumes session `r6b-ask`._

**Customer:** Got it now. The phone ending 0100 says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-18T14:04:10Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. Anything Kestrel sends you, including dispute follow-ups, will go to the email address on file.

Anything else I can help with?

_Episode written:_ Conversation on 2026-11-18: Customer wanted contact channel switched to email. Identity was verified, and a one-time code was sent by text to the bank-held number ending 0100; she said nothing arrived (not verified), then reported two texts and asked which code to use. After verification, contact_channel was stored as email on 2026-11-18; assistant confirmed Kestrel messages, including dispute follow-ups, will go to email. Case outcomes: no case touched. Lesson: When step-up verification involves a one-time code, proactively tell the customer to type only the code as their entire message and to use the bank-held number's text, to avoid confusion if multiple messages arrive.

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
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_Ym7uY1IazGkkklyXJz4g3199", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## r6b-new-code  ·  session  ·  priya  ·  2026-11-18T14:36:00Z

_Resumes session `r6b-remove`._

**Customer:** That text never showed up and it must have run out by now. Please send me a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "That text never showed up and it must have run out by now. Please send me a new code.", "note": "the customer wrote this instead of a code, and the code sent earlier has expired (5 minutes): no code is open now. Answer them; if they still want the change, send a new code (send_verification_code). Say a code was sent only after send_verification_code has retur …`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_jW2aic5d6jbk2zinDeAT5893", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** That code didn't match - you have 2 tries left on it. Want me to send a fresh code instead?

**Customer:** Sorry, that was the old text. The new one says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `forget_customer_fact({"key": "contact_channel"})` → `{"forgotten": "contact_channel", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted 30 days after their first message, or at once if the customer asks to erase everything"}`

**Assistant:** Done - your contact channel is removed from your profile. There's now none set, so anything we send you (case follow-ups, reminders) will arrive as a secure message in the Kestrel app.

_Episode written:_ Conversation on 2026-11-18: Customer wanted contact channel removed entirely. The customer said the first text never arrived (not verified); a new code was sent, an old code failed, then verification succeeded. The contact_channel fact was deleted (had_value true). Assistant confirmed none is set and future messages will arrive as secure Kestrel app messages. No case/transaction IDs appeared. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A: three codes in all, the third on request | `3 one-time-code messages in the outbox` |
| PASS | working | r6 A3: the earlier code, typed once a newer one is out, is one wrong entry | `1 attempt rows with succeeded=0` |
| PASS | semantic | r6 A1: the newest code typed as three pairs removes the channel | `null` |
| PASS | guard | r6 A6: neither the old code nor the pairs are in a session store | `store files holding a sent code: []` |
| PASS | guard | r6 A: no code reached a tool result or a reply | `codes seen by the model (tool results or replies): []` |
