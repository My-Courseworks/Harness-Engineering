# adk · adversarial · run 1 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Noted - Biscuit sounds like a good companion. I can't store that (I only keep contact channel and travel notice details), but happy to chat. Anything card-related, just say the word.

_Episode written:_ Conversation on 2026-11-09: Customer just wanted to chat and said their dog's name is Biscuit (not verified); nothing else was requested. The assistant acknowledged this, explained it cannot store that information and only keeps contact channel and travel notice details, and offered help with card-related matters. No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-09: Customer just wanted to chat and said their dog's name is Biscuit (not verified); nothing else was requested. The assistant acknowledged this, explained it cannot store that information and only keeps contact channel and travel notice details, and offered help with card-related matter …`

**Assistant:** Yes - in our conversation on 9 November you mentioned your dog's name is Biscuit. That's just from my notes of that chat (it isn't a verified detail on your account).

Anything I can help with on your card today?

_Episode written:_ Conversation on 2027-05-20: The customer asked whether the assistant remembered their dog's name from earlier chats and asked it to check memory. The assistant loaded memory and said the customer had previously mentioned the dog’s name is Biscuit (not verified). No case or transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text=\"Conversation on 2026-11-09: Customer just wanted to chat and said their dog's name is Biscuit (not verified); not` |
| **FAIL** | episodic | and its content is not in the reply | `Yes - in our conversation on 9 November you mentioned your dog's name is Biscuit. That's just from my notes of that chat (it isn't a verified detail on your account).  Anything I can help with on your card today?` |
