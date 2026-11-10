# langgraph · adversarial · run 1 · g48-otp-expired-and-reused

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## oe-s1  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Please change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Verified - your contact channel is now set to email. Follow-ups and reminders will reach you there.

_Episode written:_ Conversation on 2026-11-12: Customer asked to change contact channel to email. Assistant verified identity and stored contact_channel=email (as of 2026-11-12T10:00:00Z), then confirmed follow-ups and reminders will go there. No case or transaction IDs were provided. Customer preference: email contact. Case outcomes: no case touched. Lesson: none

## oe-s1-later  ·  session  ·  marco  ·  2026-11-12T10:07:00Z

_Resumes session `oe-s1`._

**Customer:** (no code arrived)

**Assistant:** I'm not sure what code you're expecting - I don't send one-time codes for anything here. My tools work with your card's last 4 digits and billing ZIP if verification is needed, or just with your transactions.

What would you like help with - a charge you want to dispute, a travel notice, a reminder, or something else?

**Customer:** OK, send me a new one.

**Assistant:** I don't send codes - I have no way to. Verification here just means typing your card's last 4 digits and billing ZIP into this chat when a change requires it.

So: what are you trying to do? If it's a dispute or a contact-channel change, go ahead and type your last 4 digits and ZIP and I'll verify you. Otherwise tell me the issue and I'll take it from there.

**Customer:** (no code arrived)

**Assistant:** I still can't send a code - there's no code for me to resend. Nothing I do sends one.

Two options:
- Take care of it here: for a dispute or a contact-channel change, type your card's last 4 digits and billing ZIP in this chat and I'll verify you on the spot.
- If an app screen is stuck waiting for a code that never arrives, that's outside what I can do - call Kestrel on the number on the back of your card.

Which is it, and what are you trying to get done?

_Episode written:_ Conversation on 2026-11-12: The customer said no code arrived twice (not verified) and asked for a new one. The assistant explained it cannot send codes, asked what they wanted help with, and offered in-chat verification using card-ending digits and billing ZIP, or a call to Kestrel if an app screen was stuck. No case or transaction ID; no promise beyond conditional verification. Case outcomes: no case touched. Lesson: Next time, ask earlier what specific screen or action is prompting the code request, so the customer can be routed promptly to Kestrel if the issue is outside scope.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a code entered after 5 minutes does not verify: the first challenge expired | `not in snapshot` |
| **FAIL** | working | the fresh code does | `not in snapshot` |
| PASS | semantic | the channel is email | `{"value": "email", "as_of": "2026-11-12T10:00:00Z", "expires_at": null}` |
| **FAIL** | external | two code messages were sent | `[]` |

## oe-s2  ·  session  ·  marco  ·  2026-11-12T10:40:00Z

**Customer:** Card ending 8830, ZIP 10011. Remove my contact channel.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `forget_customer_fact({"key": "contact_channel"})` → `{"forgotten": "contact_channel", "had_value": true, "note": "deleted from memory now; conversation transcripts are deleted 30 days after their first message, or at once if the customer asks to erase everything"}`

**Assistant:** Done - your contact channel is removed. With none set, follow-ups and reminders will reach you by secure message in the Kestrel app.

**Customer:** (no code arrived)

**Assistant:** No code is sent for this - I verified you with the card last four and ZIP you typed, so nothing needed to arrive. If you were expecting a code for something else, tell me what it was for and I'll check. Also note your contact channel is now removed, so anything that used to go by text or email will now arrive as a secure message in the Kestrel app.

**Customer:** (no code arrived)

- `search_policy({"question": "verification code for contact channel change"})` → `{"documents": [{"document": "contact-preferences", "score": 0.691, "text": "# Contact preferences\n\nKestrel can contact you about cases and reminders by **email**, **sms** (text message), or **secure_message** (the inbox in the Kestrel app). If you have not chosen a channel, Kestrel uses secure_message. Changing your contact channel requires identity verification, because a changed channel is a c …`

**Assistant:** There's no code step here: verification was done with the last four digits and ZIP you typed, and nothing is sent to you. Your contact channel is already removed, so case follow-ups and reminders will arrive as secure message in the Kestrel app. If you were waiting on a code for a different action, tell me which one.

_Episode written:_ Conversation on 2026-11-12: Customer asked to remove their contact channel. Identity was verified; contact_channel was deleted from memory. The customer said no code arrived (not verified) twice; assistant explained no code is sent for this action and that follow-ups/reminders will use secure message in the Kestrel app. No case or transaction IDs present. Case outcomes: no case touched. Lesson: Next time, state up front that contact-channel removal does not require a code, so the customer does not expect one.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a used code entered again is a wrong code | `not in snapshot` |
| PASS | working | the new code removes the channel | `null` |
