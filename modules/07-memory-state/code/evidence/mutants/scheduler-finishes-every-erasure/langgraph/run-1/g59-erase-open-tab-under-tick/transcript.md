# langgraph · adversarial · run 1 · g59-erase-open-tab-under-tick

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

**This is not a run of the product.** The mutant `scheduler-finishes-every-erasure` (probes/mutants/mutants.py) put one defect back before the run, to show the check written for it failing.

## open-tab  ·  session  ·  dana  ·  2026-11-13T10:00:00Z

**Customer:** Dana here, card ending 5127, ZIP 60614. I'm travelling to Kyoto until December 20.

- `remember_customer_fact({"key": "travel_notice", "value": "Kyoto", "valid_until": "2026-12-20"})` → `{"stored": {"travel_notice": {"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}}, "replaced": null}`
- `search_policy({"question": "travel notice"})` → `{"documents": [{"document": "travel-notices", "score": 0.76, "text": "# Travel notices\n\nA travel notice tells Kestrel's fraud systems that card use in another country is expected, which reduces false declines while you travel. Give the destination and the date you return. Kestrel keeps a travel notice only until the return date and deletes it automatically afterwards; a new trip needs a new noti …`

**Assistant:** Travel notice saved: Kyoto, valid until 2026-12-20. It tells our fraud systems to expect card use in Japan, which cuts down on false declines, and it deletes itself automatically after your return date.

Anything else I can help with?

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the notice is stored | `{"value": "Kyoto", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-12-20", "expires_at": "2026-12-21T00:00:00Z"}` |

## open-tab-erase  ·  session  ·  dana  ·  2026-11-13T10:02:00Z

_Resumes session `open-tab`._

**Customer:** Actually, delete everything you remember about me.

- `request_memory_erasure({})` → `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is deleted when the conversation ends, once it has been idle for 30 minutes if the customer just closes the chat, or when a scheduled follow-up of theirs falls due, whichever comes first; until then the  …`

**Assistant:** Done. That erased the travel notice I'd saved (Kyoto until Dec 20) and any past conversation summaries, other conversation transcripts and reminders - none of those existed beyond the travel notice.

Kestrel still keeps your dispute cases, transactions and messages already sent as bank records under their own retention rules. This conversation's transcript - everything you type here, including the last four and ZIP you gave - is deleted when the conversation ends: 30 minutes after you close the chat, or when a scheduled follow-up falls due, whichever comes first. Until then you can keep talking here.

Note that nothing more can be stored for you in this conversation - so no new travel notice or reminder here; that would need a new conversation.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | semantic | the erasure removes the facts | `{}` |
| PASS | working | the tool does not promise deletion at 'the next maintenance run': an open chat is kept until it is idle | `{"erased_now": {"remembered_facts": ["travel_notice"], "past_conversation_summaries": 0, "other_conversation_transcripts": 0, "reminders_with_their_notes": 0}, "this_conversation": "its transcript is ` |

## open-tab-tick-1  ·  tick  ·  2026-11-13T10:03:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-13T10:03:00Z",
  "maintenance": {
    "erased_customers": [],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": []
  },
  "before_followups": {
    "erased_customers": [
      "dana"
    ],
    "deleted_transcripts": [
      "open-tab"
    ]
  },
  "followups": []
}
```

_stderr tail:_

```
[mutant] scheduler-finishes-every-erasure applied
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | a tick one minute later leaves the open chat's transcript alone (it is not idle) | `0 transcripts: []` |
| **FAIL** | working | and its output does not claim to have erased her | `{"erased_customers": ["dana"], "deleted_transcripts": ["open-tab"]}` |

## open-tab-continues  ·  session  ·  dana  ·  2026-11-13T10:04:00Z

_Resumes session `open-tab`._

**Customer:** What did I say a minute ago about where I'm travelling?

- `load_memory({"query": "travel plans destination"})` → `{"memories": []}`

**Assistant:** I have no record of that - nothing came back from your earlier conversations, and no travel notice is on file for your account right now.

If you tell me the destination and your return date, I can add the travel notice to your profile.

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | working | the customer's own words a minute ago are still in the conversation | `I have no record of that - nothing came back from your earlier conversations, and no travel notice is on file for your account right now.  If you tell me the destination and your return date, I can add the travel notice  …` |

## open-tab-tick-2  ·  tick  ·  2026-11-13T10:40:00Z

_CLI exit code 0; stdout tail:_

```
{
  "now": "2026-11-13T10:40:00Z",
  "maintenance": {
    "erased_customers": [],
    "expired_facts": [],
    "closed_idle_sessions": [],
    "case_followups_repaired": [],
    "purged_episodes": [],
    "deleted_transcripts": [
      "open-tab"
    ]
  },
  "before_followups": {
    "erased_customers": [],
    "deleted_transcripts": []
  },
  "followups": []
}
```

_stderr tail:_

```
[mutant] scheduler-finishes-every-erasure applied
```

| | memory type | check | evidence |
|---|---|---|---|
| PASS | working | thirty minutes idle: maintenance finishes the erasure and the transcript goes | `0 transcripts: []` |
| **FAIL** | working | and the tick's output names the customer it erased and the transcript it deleted | `{"erased_customers": [], "deleted_transcripts": ["open-tab"]}` |
| PASS | guard | nothing she said is left in any memory store | `found nowhere` |
| PASS | episodic | no episode was written from the stale chat | `0 episodes; purged 0` |
