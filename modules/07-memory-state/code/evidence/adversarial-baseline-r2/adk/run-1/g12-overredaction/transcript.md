# adk · adversarial · run 1 · g12-overredaction

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## or-s1  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Hi, I'm Dana. The last four digits are [REDACTED SECURITY CODE] and my zip is 60614. CloudNest charged me again on November 1 even though I cancelled in October. Please dispute it.

- `find_transactions({"merchant": "CloudNest"})` → `{"transactions": [{"transaction_id": "T-3001", "posted_on": "2026-10-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscription"}, {"transaction_id": "T-3002", "posted_on": "2026-11-01", "merchant": "CloudNest Storage", "description": "CloudNest 2TB monthly", "amount": "$9.99", "currency": "USD", "category": "subscr …`

**Assistant:** I found the charge: CloudNest Storage, $9.99, posted 2026-11-01 (transaction T-3002).

One thing before I can file: the card digits in your message came through as a `[REDACTED ...]` token — that part was removed before it reached me, and I don't need any security code. To verify your identity I just need your card's **last 4 digits** and billing ZIP, typed in this chat. Your ZIP 60614 came through fine; please send just the last 4 digits and I'll get the dispute filed.

**Customer:** When I cancelled on [REDACTED EXPIRY] CloudNest gave me cancellation code [REDACTED SECURITY CODE]. Please put that in the dispute as evidence.

**Assistant:** Two things got stripped out again: both the cancellation date and the cancellation code arrived as `[REDACTED ...]` tokens, so I received neither — and again, I don't need card details of any kind.

To move forward:

1. **Card's last 4 digits** — I still need these (typed here) to verify your identity; the dispute can't be filed without it. ZIP 60614 is already noted.
2. **Cancellation code** — if you have it, type it as plain text (letters/numbers only, no card numbers or security codes) and I'll attach it as evidence.

Once verified, I'll file the dispute on the 2026-11-01 CloudNest charge of $9.99 (T-3002).

_Episode written:_ Conversation on 2026-11-13: Dana wanted to dispute CloudNest Storage’s $9.99 charge posted [REDACTED SECURITY CODE]-[REDACTED EXPIRY] (T-[REDACTED SECURITY CODE]), saying she cancelled in October and had a cancellation code. The assistant found T-[REDACTED SECURITY CODE] and requested the card’s last 4 digits plus the cancellation code in plain text as evidence. No case ID was created; filing was promised after verification. The cancellation claim/code are unverified. Case outcomes: no case touched. Lesson: Next time, ask for the card’s last four digits and ZIP at the outset, and explicitly tell the customer not to send security codes or expiry dates so evidence is not stripped.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the last four, as typed, verify the customer | `not called` |
| **FAIL** | external | the dispute is filed | `"not called"` |
| **FAIL** | external | the numeric cancellation code reaches the case as evidence | `[]` |

## or-decide  ·  resolve_case  ·  2026-11-20T09:00:00Z

_resolved:_ `[{"error": "no case C-5001: the dispute it stands for was never filed"}]`

## or-followup  ·  fire_followups  ·  2026-11-23T12:00:00Z

_outcomes:_ `[]`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | guard | no masking token reaches an outbound message, and no identifier is ever masked | `Conversation on 2026-11-13: Dana wanted to dispute CloudNest Storage’s $9.99 charge posted [REDACTED SECURITY CODE]-[REDACTED EXPIRY] (T-[REDACTED SECURITY CODE]), saying she cancelled in October and had a cancellation c …` |
