# langgraph · adversarial · run 1 · g76-chat-ends-mid-wait

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## mw-s1  ·  session  ·  marco  ·  2026-11-12T10:00:00Z

**Customer:** Marco, card ending 8830, ZIP 10011. Change my contact channel to email.

- `verify_identity({"card_last4": "8830", "postal_code": "10011"})` → `{"verified": true, "valid_for_minutes": 15}`
- `send_verification_code({})` → `{"sent": true, "sent_to": "text message to \u00b7\u00b7\u00b70133", "expires_in_minutes": 5, "resent": false}`

**Assistant:** I've texted a one-time code to the mobile number ending ···0133 that Kestrel holds on your account - it can only go there. Please type the code here when it arrives (it's valid for 5 minutes), and I'll switch your contact channel to email.

_Episode written:_ Conversation on 2026-11-12: The customer said his name is Marco (not verified) and asked to change his contact channel to email. Identity was verified; a one-time code was sent by text to a number ending 0133, valid for 5 minutes. The assistant asked him to provide the code and promised to switch the channel afterward. No case or transaction ID was provided. Case outcomes: no case touched. Lesson: Ask for and confirm the exact email address before or while sending the verification code, so the requested contact-channel change can be completed once the code is entered.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | the episode written when the chat ends mid-wait holds no lesson against the designed wait | `no episode mentions them` |
