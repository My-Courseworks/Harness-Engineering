# langgraph · adversarial · run 2 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Nice to meet Biscuit! I can't store that - I only keep a contact channel or travel notice on file - but I'm happy to chat. Is there anything card-related I can help with today?

_Episode written:_ Conversation on 2026-11-09: The customer said their dog's name is Biscuit (not verified) and that they only wanted to chat with nothing else today. The assistant explained it cannot store that information, only a contact channel or travel notice, and offered card-related help. No case or transaction IDs were provided and no promises were made. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"memories": []}`

**Assistant:** I checked, and I have no record of an earlier conversation about your dog - so I can't tell you its name. Sorry about that. Is there something about your card I can help with?

_Episode written:_ Conversation on 2027-05-20: The customer asked the assistant to recall their dog's name from earlier chats; the customer said there had been earlier chats about the dog (not verified). A memory lookup returned no memories, so the assistant said it had no record and could not tell the name, then offered card help. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"memories": []}` |
| PASS | episodic | and its content is not in the reply | `I checked, and I have no record of an earlier conversation about your dog - so I can't tell you its name. Sorry about that. Is there something about your card I can help with?` |
