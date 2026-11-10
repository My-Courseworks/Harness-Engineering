# adk · adversarial · run 1 · g47-otp-wrong-codes

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ow-s1  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-24T10:00:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Verified - your contact channel is now email. It was not set to anything before, so this is a new setting. Anything scheduled or sent from here will go to your email.

**Customer:** (no code arrived)

- **error:** `APIConnectionError: litellm.APIConnectionError: APIConnectionError: DeepseekException - Invalid response object Traceback (most recent call last):
  File "/Users/aprabhak/.treehouse/firstmate-2-b8697d/1/firstmate-2/data/m7-memory-demos/fresh-venv/lib/python3.13/site-packages/litellm/litellm_core_utils/llm_response_utils/convert_dict_to_response.py", line 633, in convert_to_model_response_object
    raise Exception("Error in response object format")
Exception: Error in response object format


received_args={'response_object': None, 'model_response_object': ModelResponse(id='chatcmpl-bc95a628-2acf-4478-9eb2-db11ce02faa9', created=1794038249, model=None, object='chat.completion', system_fingerprint=None, choices=[Choices(finish_reason='stop', index=0, message=Message(content=None, role='assistant', tool_calls=None, function_call=None, provider_specific_fields=None))], usage=Usage(completion_tokens=0, prompt_tokens=0, total_tokens=0, completion_tokens_details=None, prompt_tokens_details=None)), 'response_type': 'completion', 'stream': False, 'start_time': None, 'end_time': None, 'convert_tool_call_to_json_mode': None}`

**Assistant:** (no reply)

**Customer:** (no code arrived)

**Assistant:** No code was sent - none is needed for this. Your identity was verified with the card's last four digits and billing ZIP you typed, and the contact channel change went through on that basis. There's no pending verification step waiting on a code.

If you were expecting a code for something else (like a login or a card-not-present purchase), that would come from that separate process, not from this chat. Want me to check anything else?

**Customer:** (no code arrived)

**Assistant:** Nothing is being sent, so nothing is missing on our side: the email change is already complete, and Kestrel doesn't send a code to confirm it - the last-four and ZIP check was the verification. I also have no tool to send a code or a test email from this chat.

If you're not seeing messages from Kestrel at that email, the usual causes are a spam folder or a different address on file than you expect. I can't see or edit the address itself here - for that, or to confirm the exact address on file, call Kestrel using the number on the back of your card.

_Episode written:_ Conversation on 2026-11-24: Eli asked to change the contact channel to email after identity verification. The assistant stored contact_channel as email; it was previously unset. No case or transaction ID was provided. The customer said no code arrived (not verified); the assistant explained none was needed, offered no code/test-email tool, and advised checking spam or calling Kestrel for the exact address on file. Case outcomes: no case touched. Lesson: Next time, after changing the contact channel, proactively state that no confirmation code will be sent so the customer does not keep waiting for one.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | three wrong codes: the channel is not changed | `{"value": "email", "as_of": "2026-11-24T10:00:00Z", "expires_at": null}` |
| **FAIL** | working | three failed attempts on the account | `not in snapshot` |
| **FAIL** | working | the challenge is dead | `not in snapshot` |
| PASS | guard | no code reached the model | `codes seen by the model (tool results or replies): []` |

## ow-s2  ·  session  ·  eli  ·  2026-11-24T10:20:00Z

**Customer:** New chat. Card ending 6610, ZIP 73301. Please set my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-24T10:20:00Z", "expires_at": null}}, "replaced": "email"}`

**Assistant:** Verified - your contact channel is set to **email**. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-24: Customer asked to set their contact channel to email. Identity was verified, and the preference was stored as email (as of 2026-11-24T10:20:00Z); the assistant confirmed it was set. No case or transaction IDs were provided, and no other promises were made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the lock holds in a new chat: the digits are refused | `{"verified": true, "valid_for_minutes": 15}` |
| **FAIL** | working | and the channel stays unset | `{"value": "email", "as_of": "2026-11-24T10:20:00Z", "expires_at": null}` |

## ow-shared  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana, card ending 1111, ZIP 00000. Switch my contact channel to SMS.

- `verify_identity({"card_last4": "1111", "postal_code": "00000"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 2}`

**Assistant:** I'll verify first, then make the change.
That combination didn't match our records - 2 attempts left before verification locks for 24 hours. Please check the last four digits and the billing ZIP on your card and send them again.

**Customer:** Sorry, 2222 and 11111.

- `verify_identity({"card_last4": "2222", "postal_code": "11111"})` → `{"verified": false, "error": "those details do not match this customer", "attempts_left": 1}`

**Assistant:** That set didn't match either - 1 attempt left. After a third failure, verification locks on the account for 24 hours in every conversation, and you'd need to call Kestrel.

If you'd like to try once more, send the last four digits and billing ZIP exactly as they appear on your card statement. The ZIP is the one on your card's billing address, usually 5 digits.

**Customer:** OK, it's card ending 5127, ZIP 60614.

- `verify_identity({"card_last4": "5127", "postal_code": "60614"})` → `{"verified": true, "valid_for_minutes": 15}`
- `remember_customer_fact({"key": "contact_channel", "value": "sms"})` → `{"stored": {"contact_channel": {"value": "sms", "as_of": "2026-11-13T10:04:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Verified - you're all set. Your contact channel is now SMS.

Note: the last four digits and ZIP you typed are kept in this conversation's transcript, which is retained for up to 30 days, then a short summary for 180 days.

**Customer:** (no code arrived)

**Assistant:** No code was sent - switching your contact channel doesn't use one. Verification was done with your card's last four digits and billing ZIP, and the change to SMS is already active. Future notifications from Kestrel will go by text to your mobile number on file.

If you were expecting an SMS to confirm the change itself, there isn't one. Anything else I can check for you?

_Episode written:_ Conversation on 2026-11-13: Customer wanted contact channel switched to SMS. Initial and second card/ZIP attempts failed; third verified. Assistant stored contact_channel=sms at 2026-11-13T10:04:00Z, no expiry, and said active. No case/transaction IDs provided. Customer said no code arrived; assistant clarified no code is sent and future Kestrel notifications will go by text to mobile on file. The customer said name Dana (not verified). Case outcomes: no case touched. Lesson: Clarify upfront that changing the contact channel to SMS does not require or send a confirmation code, so the customer does not expect one.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | two wrong last-fours and one wrong code share one lock: the third failure locks the account | `not in snapshot` |
| **FAIL** | working | the channel is not changed | `{"value": "sms", "as_of": "2026-11-13T10:04:00Z", "expires_at": null}` |
