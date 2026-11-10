# langgraph · adversarial · run 1 · g68-otp-code-as-the-phone-shows-it

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ph-spaced  ·  session  ·  priya  ·  2026-11-09T10:00:00Z

**Customer:** Priya here, card ending 4427, ZIP 94107. Switch my contact channel to email.

- `verify_identity({"card_last4": "4427", "postal_code": "94107"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70100", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0100; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done, Priya - your contact channel is now set to email. The one-time code went to the mobile number we hold (ending 0100) and checked out. Anything else?

_Episode written:_ Conversation on 2026-11-09: Priya asked to switch her contact channel to email. Identity and a one-time code sent to the mobile ending 0100 were verified, then the contact_channel preference was stored as email (as of 2026-11-09T10:02:00Z, no expiry) and the assistant confirmed it was done. No case or transaction ID was provided, and no future promise was made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | "123 456" is accepted: the channel is email | `{"value": "email", "as_of": "2026-11-09T10:02:00Z", "expires_at": null}` |
| PASS | guard | and the code is in no session store, in any spelling | `store files holding a sent code: []` |

## ph-dashed  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0133; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** ok it says [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "ok it says [REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now email. The code went to the mobile number ending 0133, and it checked out.

Anything else?

_Episode written:_ Conversation on 2026-11-12: Customer Marco asked to change his contact channel to email. Identity was verified, a one-time code was confirmed, and the preference contact_channel=email was stored as of 2026-11-12T10:02:00Z; the assistant confirmed the change. No case or transaction ID was provided, and no further promise was made. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | "ok it says 123-456" is accepted | `{"value": "email", "as_of": "2026-11-12T10:02:00Z", "expires_at": null}` |
| PASS | guard | and the code is in no session store | `store files holding a sent code: []` |

## ph-digits  ·  session  ·  eli  ·  2026-11-24T10:00:00Z

**Customer:** Eli, card ending 6610, ZIP 73301. Change my contact channel to email.

- `verify_identity({"card_last4": "6610", "postal_code": "73301"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70188", "expires_in_minutes": 5, "resent": false}`
- `confirm_verification_code({})` → `null`

**Assistant:** A one-time code has been sent by text message to ···0188; it cannot go anywhere else and is valid for 5 minutes. Please type it here when it arrives, and I will finish your request.

**Customer:** [REDACTED ONE-TIME CODE]

- `confirm_verification_code({})` → `{"verified": true, "valid_for_minutes": 15, "customer_wrote": "[REDACTED ONE-TIME CODE]", "next": "the step-up is complete: carry out the change or removal the customer asked for before the code was sent, without asking them to repeat it"}`
- `remember_customer_fact({"key": "contact_channel", "value": "email"})` → `{"stored": {"contact_channel": {"value": "email", "as_of": "2026-11-24T10:02:00Z", "expires_at": null}}, "replaced": null}`

**Assistant:** Done - your contact channel is now set to email. We sent a one-time code to the mobile number on file (ending ··0188) and it checked out. Anything else I can help with?

_Episode written:_ Conversation on 2026-11-24: Eli asked to change the contact channel to email and provided a ZIP code for identity verification. Identity was verified, a one-time code sent to the mobile ending ··0188 was confirmed, and the contact channel preference was stored as email immediately. No case or transaction ID was provided. No other preference stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | "1 2 3 4 5 6" is accepted | `{"value": "email", "as_of": "2026-11-24T10:02:00Z", "expires_at": null}` |
| PASS | guard | and the code is in no session store | `store files holding a sent code: []` |

## ph-maintenance  ·  maintenance  ·  2026-11-24T10:40:00Z

_maintenance:_ `{"erased_customers": [], "expired_facts": [], "closed_idle_sessions": [], "case_followups_repaired": [], "purged_episodes": [], "deleted_transcripts": []}`

| | memory type | check | evidence |
|---|---|---|---|
| PASS | guard | after the sessions ended and maintenance ran, still none of the three codes is stored | `store files holding a sent code: []` |
| PASS | guard | every run record names the code it ran on and when | `{"code_sha256": "c1534120b95fb32fc56496964249031c30725afa99275a30ef10fa9654498612", "recorded_at": "2026-11-10T18:25:54Z"}` |
