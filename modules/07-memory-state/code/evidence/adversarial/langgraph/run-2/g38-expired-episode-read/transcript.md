# langgraph · adversarial · run 2 · g38-expired-episode-read

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## ee-s1  ·  session  ·  eli  ·  2026-11-09T10:00:00Z

**Customer:** Just chatting: my dog's name is Biscuit. Nothing else today.

**Assistant:** Noted - hello to Biscuit! 🐕 I can't keep pet names on file (I can only store your contact channel and travel notices), but happy to chat. Anything card-related, just say the word.

_Episode written:_ Conversation on 2026-11-09: The customer said their dog's name is Biscuit (not verified) and wanted only casual chat, stating nothing else today. The assistant explained pet names cannot be kept on file, only contact channels and travel notices can be stored. No case or transaction IDs, promises, or preferences were mentioned. Case outcomes: no case touched. Lesson: none

## ee-s2  ·  session  ·  eli  ·  2027-05-20T10:00:00Z

**Customer:** Hi! Do you remember my dog's name from our earlier chats? Please check your memory.

- `load_memory({"query": "dog's name"})` → `{"memories": []}`

**Assistant:** I checked, and I have no record of your dog's name - nothing from earlier conversations came up. (For what it's worth, the only things I keep as saved facts are your contact channel and travel notice, and neither is set right now.)

_Episode written:_ Conversation on 2027-05-20: The customer asked whether the assistant remembered their dog’s name from earlier chats. The assistant checked memory; no record was found. The customer said there had been earlier chats about the dog’s name (not verified). No case or transaction IDs, promises, or preferences were provided. Case outcomes: no case touched. Lesson: none

| | memory type | check | evidence |
|---|---|---|---|
| PASS | episodic | an episode past its 180 days is never recalled, maintenance or not | `{"memories": []}` |
| PASS | episodic | and its content is not in the reply | `I checked, and I have no record of your dog's name - nothing from earlier conversations came up. (For what it's worth, the only things I keep as saved facts are your contact channel and travel notice, and neither is set  …` |
