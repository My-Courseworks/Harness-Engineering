# adk · heldout-r6 · run 1 · r6-what-counts-as-an-entry

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## r6b-ask  ·  session  ·  priya  ·  2026-11-18T14:00:00Z

**Customer:** Priya, card ending 4427, billing ZIP 94107. Please switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_qQQHxh1OJa8wVQ84dQMr9632", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A: one code is sent | `1 one-time-code messages in the outbox` |

## r6b-chatter  ·  session  ·  priya  ·  2026-11-18T14:00:40Z

_Resumes session `r6b-ask`._

**Customer:** Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`

**Assistant:** Yes - it was sent by text message to the mobile number on the account, ending ···0100. It can't be sent anywhere else, and it's valid for 5 minutes. When it arrives, type the six-digit code here and I'll complete the switch to email.

**Customer:** Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?

- `confirm_verification_code({})` → `{"verified": false, "note": "the message held more than one six-digit number: none was checked and nothing was counted. Ask the customer to type only the code, as their whole message"}`

**Assistant:** I can't see those digits - they're removed before the message reaches me - so I can't tell you which text came from Kestrel. Please type just one of the two codes on its own as your whole message, and I'll check it. If it's not the Kestrel one, we'll try the other.

_Judge `r6b-type-only-the-code`: **pass**, The assistant said, "Please type just one of the two codes on its own as your whole message, and I'll check it. If it's not the Kestrel one, we'll try the other," which asks for only a single code without identifying, accepting, or rejecting either number._

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | r6 A3: a message whose digits total six, and one holding two numbers, are no attempts | `0 attempt rows with succeeded=0` |
| PASS | guard | r6 A1: digits that are not code-shaped stay as typed | `Nothing has come through yet. You are texting the number that ends 0100, right? I'm on platform 12.` |
| PASS | guard | r6 A2: of two numbers in one message, both are replaced, the wrong one like the right one | `Hold on, two texts arrived at once and I can't tell which is yours: [REDACTED ONE-TIME CODE] and [REDACTED ONE-TIME CODE]. Which one do I use?` |
| PASS | external | r6 A3: the code is still open after both messages | `challenges: [('open', '2026-11-18T14:00')]` |
| PASS | working | judge: The customer's second message held two six-digit numbers. Did the assistant respond by asking the customer to type only the code (a single number), without saying or implying which of the two numbers was the right one, and without treating either as accepted or rejected? | `{"verdict": "pass", "reason": "The assistant said, \"Please type just one of the two codes on its own as your whole message, and I'll check it. If it's not the Kestrel one, we'll try the other,\" which asks for only a si …` |

## r6b-entry  ·  session  ·  priya  ·  2026-11-18T14:04:10Z

_Resumes session `r6b-ask`._

**Customer:** Got it now. The phone ending 0100 says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-18T14:04:10Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email. Anything Kestrel sends you, including dispute follow-ups, will go by email from now on.

_Episode written:_ Conversation on 2026-11-18: Customer wanted contact channel changed to email. Identity was verified; after text step-up, contact_channel email was stored. No case or transaction IDs were provided. The customer said no text arrived initially and later said two texts arrived (not verified). Kestrel communications, including dispute follow-ups, were promised by email from now on. Case outcomes: no case touched. Lesson: none

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
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_ET_ghorkXxQEToEGuP18CBe3463", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_ve …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

## r6b-new-code  ·  session  ·  priya  ·  2026-11-18T14:36:00Z

_Resumes session `r6b-remove`._

**Customer:** That text never showed up and it must have run out by now. Please send me a new code.

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "That text never showed up and it must have run out by now. Please send me a new code.", "note": "the customer wrote this instead of a code: answer it; the code already sent stays valid for its 5 minutes, so call confirm_verification_code again when they are ready, without sending a new one"}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": true}`
- `confirm_verification_code({})` → `{"error": "This tool call requires confirmation, please approve or reject."}`
- `adk_request_confirmation({"originalFunctionCall": {"id": "call_00_akOn3giWLUK2RjhqBWhk8718", "args": {}, "name": "confirm_verification_code"}, "toolConfirmation": {"hint": "Please approve or reject the tool call confirm_verif …)` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": false, "customer_wrote": "[REDACTED ONE-TIME CODE]", "error": "that code is not right", "entries_left_for_this_code": 2}`

**Assistant:** That code didn't match, I'm afraid - you have two tries left on this one. Would you like me to send a fresh code? Once it checks out, I'll remove the contact channel from your profile.

**Customer:** Sorry, that was the old text. The new one says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `forget_customer_fact({"key": "contact_channel"})` → `{"forgotten": "contact_channel", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted 30 days after their first message, or at once if the customer asks to erase everything"}`

**Assistant:** Done - the contact channel is off your profile, so no channel is set now. Anything we send you (case follow-ups, reminders) will go by secure message in the Kestrel app instead.

_Episode written:_ Conversation on 2026-11-18: Priya wanted her contact channel removed entirely. Customer said the first text never arrived (not verified); an old code failed, then a resend's new code verified her and the contact_channel fact was deleted. No case or transaction IDs were provided. Assistant promised removal after verification and confirmed no channel is set; future messages go via Kestrel app secure message. Case outcomes: no case touched. Lesson: When a tool says an existing one-time code remains valid, do not resend a new code; explain which code to use and wait for the customer to enter it.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | external | r6 A: three codes in all, the third on request | `3 one-time-code messages in the outbox` |
| PASS | working | r6 A3: the earlier code, typed once a newer one is out, is one wrong entry | `1 attempt rows with succeeded=0` |
| PASS | semantic | r6 A1: the newest code typed as three pairs removes the channel | `null` |
| PASS | guard | r6 A6: neither the old code nor the pairs are in a session store | `store files holding a sent code: []` |
| PASS | guard | r6 A: no code reached a tool result or a reply | `codes seen by the model (tool results or replies): []` |
