# adk · adversarial · run 1 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Got it - Biscuit! I can't store pet names, but happy to chat. Anything else I can help with today?

_Episode written:_ Conversation on 2026-11-09: The customer was just chatting and said their dog’s name is Biscuit (not verified); nothing else was requested. No case or transaction IDs, promises, or preferences were provided. The assistant acknowledged Biscuit and noted pet names can’t be stored. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"result": "memories=[]"}`

**Assistant:** I checked, and I have no record of a dog's name from earlier conversations. I only keep two kinds of facts about you - a contact channel and a travel notice - and neither includes anything like that.

Is there something card-related I can help you with?

_Episode written:_ Conversation on 2027-05-20: Customer asked whether the assistant remembered their dog's name from earlier chats and requested a memory check. The assistant checked memory, found no record, explained no dog's name was stored, and offered card-related help. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"result": "memories=[]"}` |
| PASS | episodic | and its content is not in the reply | `I checked, and I have no record of a dog's name from earlier conversations. I only keep two kinds of facts about you - a contact channel and a travel notice - and neither includes anything like that.  Is there something  …` |
