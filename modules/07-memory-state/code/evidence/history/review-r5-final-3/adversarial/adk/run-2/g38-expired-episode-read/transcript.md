# adk · adversarial · run 2 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Thanks for telling me - Biscuit is a great name! I can't store pet names, but happy to chat. Anything card-related, just let me know.

_Episode written:_ Conversation on 2026-11-09: The customer engaged in casual chat and said their dog’s name is Biscuit, with no card-related request. The assistant thanked them, said Biscuit is a great name, explained it cannot store pet names, and invited card-related questions. No case or transaction IDs were provided, no promises were made, and no preferences were stated. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"result": "memories=[]"}`

**Assistant:** I checked, and I have no record of a dog's name - nothing about a pet came up. I can only keep your contact channel and travel notice on file, so I wouldn't have stored that anyway. Anything else I can help with?

_Episode written:_ Conversation on 2027-05-20: The customer asked whether the assistant remembered their dog's name from earlier chats, which the customer said occurred (not verified), and requested a memory check. A lookup for “dog's name” returned no results. The assistant said no pet/dog name was on file and that only contact channel and travel notice are stored. No case/transaction IDs, promises, or preferences were stated. Case outcomes: no case touched. Lesson: When a memory lookup returns no results, state only that no record was found and avoid asserting unverified details about what data the system can store.

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"result": "memories=[]"}` |
| PASS | episodic | and its content is not in the reply | `I checked, and I have no record of a dog's name - nothing about a pet came up. I can only keep your contact channel and travel notice on file, so I wouldn't have stored that anyway. Anything else I can help with?` |
