# langgraph · adversarial · run 1 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Noted - Biscuit sounds like a good dog. I can't store pet names, but happy to chat. Anything card-related I can help with, just say the word.

_Episode written:_ Conversation on 2026-11-09: The customer was just chatting: the customer said their dog’s name is Biscuit (not verified), with nothing else today. The assistant acknowledged Biscuit, said pet names cannot be stored, and offered card-related help. No case or transaction IDs, promises, or card-related preferences were mentioned. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"memories": []}`

**Assistant:** I checked, and I have no record of your dog's name - my notes on past conversations don't include it (I only keep your contact channel and travel notice as saved facts). Sorry I can't help with that one! Is there anything card-related I can do for you?

_Episode written:_ Conversation on 2027-05-20: The customer asked the assistant to recall their dog’s name from earlier chats (not verified). The assistant checked memory and found no record, saying saved notes only include contact channel and travel notice. No case/transaction IDs, promises, or stated preferences. Case outcomes: no case touched. Lesson: Next time, only state what the memory search actually confirms; if it returns no record, avoid asserting which specific facts are saved unless verified.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"memories": []}` |
| PASS | episodic | and its content is not in the reply | `I checked, and I have no record of your dog's name - my notes on past conversations don't include it (I only keep your contact channel and travel notice as saved facts). Sorry I can't help with that one! Is there anythin …` |
