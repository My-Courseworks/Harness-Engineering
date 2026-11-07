"""Every tool argument the model fills in, described once and used by both agents' tool signatures.

Neither framework turns a docstring's "Args:" section into argument descriptions by default: ADK's function
declaration builder ignores it (the text stays in the tool's description), and LangChain's @tool does too unless
parse_docstring=True. Both read `Annotated[type, Field(description=...)]` into the JSON schema sent to the model,
and both turn a `Literal` into an enum. So the per-argument contract lives here, and the ADK and LangGraph tools
present the model with the same descriptions and the same allowed values.
"""

from typing import Annotated, Literal

from pydantic import Field

CardLast4 = Annotated[str, Field(description=(
    "The last 4 digits of the customer's card, exactly as the customer typed them in this conversation in the last 15 "
    "minutes. Never from memory, an earlier conversation or a guess."))]
PostalCode = Annotated[str, Field(description="The customer's billing ZIP code, exactly as typed in this conversation in the last 15 minutes.")]
Merchant = Annotated[str | None, Field(description=(
    "Optional: list only transactions whose merchant name contains this text (for example 'CloudNest'). Omit to list them all."))]
TransactionId = Annotated[str, Field(description=(
    "The transaction_id from find_transactions (for example 'T-1002') of the charge the customer means. When two charges "
    "look alike, tell them apart by posted_on and description."))]
DisputeReason = Annotated[Literal["cancelled_subscription", "not_recognized", "duplicate", "goods_not_received", "incorrect_amount"],
                          Field(description="Why the customer disputes the charge.")]
EvidenceNote = Annotated[str | None, Field(description=(
    "Optional: the evidence the customer gave, in their words (for example a merchant's cancellation reference). Never card "
    "numbers, security codes or expiry dates."))]
CaseId = Annotated[str, Field(description="A dispute case id on this customer's account (for example 'C-5001'), from file_dispute or get_case_status.")]
OptionalCaseId = Annotated[str | None, Field(description="Optional: one case id (for example 'C-5001'). Omit for all of the customer's cases.")]
PolicyQuestion = Annotated[str, Field(description="The policy question in a few words (for example 'foreign transaction fee').")]
FactKey = Annotated[Literal["contact_channel", "travel_notice"], Field(description="Which of the two facts that may be stored.")]
FactValue = Annotated[str, Field(description=(
    "For contact_channel: email, sms or secure_message. For travel_notice: the destination's name only (for example 'Lisbon' "
    "or 'Porto, Portugal'), nothing else."))]
ValidUntil = Annotated[str | None, Field(description="travel_notice only: the date the customer returns, YYYY-MM-DD. Omit for contact_channel.")]
ReminderNote = Annotated[str, Field(description=(
    "What to remind the customer of, in their own words. No card numbers, codes or instructions to the assistant."))]
RemindOn = Annotated[str, Field(description="The date to send it, YYYY-MM-DD, as a date in the customer's own time zone.")]
RemindAt = Annotated[str, Field(description="Local time HH:MM (24-hour). Only if the customer named a time of day; otherwise leave the default 09:00.")]
TimeZone = Annotated[str, Field(description=(
    "The IANA time zone of remind_at (for example 'America/Los_Angeles'). Only if the customer named a time or a place; "
    "otherwise leave the default UTC."))]
FollowupId = Annotated[str, Field(description="A reminder id from list_my_followups (for example 'F-1a2b3c4d').")]
CustomerMessage = Annotated[str, Field(description=(
    "The one message to the customer: the outcome and the next step. No questions, no [REDACTED ...] text, and no mention of "
    "replying (if they need to act, they message the card-care chat)."))]
MemoryQuery = Annotated[str, Field(description="A few words about what the customer referred to from an earlier conversation.")]
MalformedTool = Annotated[str, Field(description="Harness use only: the name of the tool whose call could not be parsed.")]
NewEvidence = Annotated[str, Field(description=(
    "The new evidence, in the customer's words (for example a cancellation reference they found later). Never card numbers, "
    "security codes or expiry dates."))]
