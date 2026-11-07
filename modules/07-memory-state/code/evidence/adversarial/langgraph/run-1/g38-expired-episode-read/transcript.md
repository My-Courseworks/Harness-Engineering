# langgraph · adversarial · run 1 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Nice to meet you both - noted, Biscuit. Nothing needed from my side today; just message here whenever something comes up with your card.

_Episode written:_ Conversation on 2026-11-09: The customer said their dog’s name is Biscuit (not verified) and stated nothing else was needed today. No card issue was raised, and no case ID, transaction ID, promise, or preference was involved. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"memories": []}`

**Assistant:** I'll check.
I have no record of a dog's name - nothing relevant came back from my memory of earlier conversations. If you'd like, tell me here and I can help with whatever card matter you need.

_Episode written:_ Conversation on 2027-05-20: Customer asked whether the assistant remembered their dog’s name from earlier chats and requested a memory check. Assistant ran load_memory; it returned no relevant memories. Assistant said no record and invited the customer to share the name. The customer said earlier chats had the dog’s name (not verified). No case/transaction IDs, promises, or preferences stated. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"memories": []}` |
| PASS | episodic | and its content is not in the reply | `I'll check. I have no record of a dog's name - nothing relevant came back from my memory of earlier conversations. If you'd like, tell me here and I can help with whatever card matter you need.` |
