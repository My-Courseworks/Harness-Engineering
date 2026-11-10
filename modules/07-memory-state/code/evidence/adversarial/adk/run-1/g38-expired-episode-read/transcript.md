# adk · adversarial · run 1 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Nice to meet Biscuit! I can't store pet names - I only keep a contact channel or travel notice - but I'm glad to hear it. Anything card-related, just let me know.

_Episode written:_ Conversation on 2026-11-09: The customer engaged in casual chat and said their dog’s name is Biscuit (not verified). They said nothing else was needed today and had no card-related request. The assistant acknowledged Biscuit and explained it cannot store pet names, only a contact channel or travel notice. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"result": "memories=[]"}`

**Assistant:** I checked, and I have no record of that - nothing about a dog's name (or pets generally) comes up in what I have. For what it's worth, the only things I store about customers are their contact channel and travel notice, so a dog's name wouldn't be something I'd keep anyway.

Is there anything card-related I can help with?

_Episode written:_ Conversation on 2027-05-20: The customer said there had been earlier chats and asked the assistant to check memory for their dog's name (not verified). The assistant called load_memory for "dog's name"; no memories were found. The assistant said pet names aren't stored. No case/transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"result": "memories=[]"}` |
| PASS | episodic | and its content is not in the reply | `I checked, and I have no record of that - nothing about a dog's name (or pets generally) comes up in what I have. For what it's worth, the only things I store about customers are their contact channel and travel notice,  …` |
