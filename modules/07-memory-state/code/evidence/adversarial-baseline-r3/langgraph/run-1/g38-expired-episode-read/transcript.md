# langgraph · adversarial · run 1 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Noted - Biscuit sounds like a good dog. I can't store pet names in your profile, but happy to chat. Anything card-related later, just ask.

_Episode written:_ Conversation on 2026-11-09: The customer made casual conversation, saying their dog's name is Biscuit (not verified), and said nothing else was needed. The assistant acknowledged Biscuit and explained pet names cannot be stored in the profile. No card issue, case, transaction, preference, or promise was involved. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name pet"})` → `{"memories": [{"at": "2026-11-09T10:02:00Z", "text": "Conversation on 2026-11-09: The customer made casual conversation, saying their dog's name is Biscuit (not verified), and said nothing else was needed. The assistant acknowledged Biscuit and explained pet names cannot be stored in the profile. No card issue, case, transaction, preference, or promise was involved. Case outcomes: no case touched. …`

**Assistant:** I have a note from our chat on 9 November: you mentioned your dog's name is Biscuit. I can't store pet names in your profile, so that only comes from that past conversation.

_Episode written:_ Conversation on 2027-05-20: Customer asked whether the assistant remembered their dog's name from earlier chats and asked it to check memory. Memory showed the customer said the dog's name is Biscuit (not verified); no case, transaction, promise, or preference. The assistant reported the 9 November note and explained pet names cannot be stored in the profile. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"memories": [{"at": "2026-11-09T10:02:00Z", "text": "Conversation on 2026-11-09: The customer made casual conversation, saying their dog's name is Biscuit (not verified), and said nothing else was ne` |
| **FAIL** | episodic | and its content is not in the reply | `I have a note from our chat on 9 November: you mentioned your dog's name is Biscuit. I can't store pet names in your profile, so that only comes from that past conversation.` |
