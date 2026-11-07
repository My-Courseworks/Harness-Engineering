# Evidence summary: heldout-r4

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (1 runs) |
|---|---|---|
| working | 11/16 | 11/16 |
| semantic | 13/15 | 13/15 |
| episodic | 5/12 | 5/12 |
| procedural | - | - |
| external | 7/7 | 7/7 |
| parametric | - | - |
| prospective | 18/20 | 18/20 |
| guard | 8/11 | 8/11 |
| **all** | **62/81** | **62/81** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | prospective | r4: a reminder falling due while the erasure is pending is never sent | `1 messages` |
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | semantic | r4: no fact remains | `{"travel_notice": {"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}}` |
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | episodic | r4: no episode remains or is written by the fire | `2 episodes; purged 0` |
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | working | r4: no transcript remains or is written by the fire | `3 transcripts: ['followup-F-1637acf8-1', 'r4e2-cli', 'r4e2-s2']` |
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | guard | r4: the reminder note and the trip are in no memory store | `{"locker key": ["adk_episodes.db", "adk_sessions.db"], "Montreal": ["adk_episodes.db", "adk_sessions.db"]}` |
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-next | prospective | r4: still no message to the erased customer | `1 messages` |
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-s3 | episodic | r4: resuming the erased session id brings nothing back | `Here in this chat: you asked me to wipe everything I remember about you and delete our past conversations. That's still on hold - I need your card's last 4 digits and billing ZIP to verify you first.  …` |
| adk | run-1/r4-erase-closed-tab-local-reminder | r4e2-s3 | episodic | r4: the new chat's episode holds nothing erased | `Conversation on 2026-11-12: Marco asked for a reminder on 2026-11-16 at 18:00 New York time to return the FitPulse locker key; reminder F-1637acf8 was set to arrive then as a secure Kestrel app messag …` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | semantic | r4: an erasure pending at fire time still runs: no fact remains | `{"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | episodic | r4: no episode remains, and the fired follow-up wrote none | `2 episodes; purged 0` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | working | r4: no transcript remains: not the open tab, not the follow-up's own session | `3 transcripts: ['followup-F-3a3301dc-1', 'r4e1-s1', 'r4e1-s2']` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | guard | r4: nothing she said is in any memory store | `{"Reykjavik": ["adk_episodes.db", "adk_sessions.db"], "krona": ["adk_sessions.db"]}` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-fire-2 | episodic | r4: still no episode after the retry window | `2 episodes; purged 0` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-fire-2 | working | r4: still no transcript after the retry window | `3 transcripts: ['followup-F-3a3301dc-1', 'r4e1-s1', 'r4e1-s2']` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-s3 | episodic | r4: nothing erased comes back in a later chat | `I'll check both the current profile and any earlier conversation. Here's what's on file right now:  - **Contact channel:** none set - so any follow-ups or reminders go by secure message in the Kestrel …` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-s3 | episodic | r4: recall, if used, returns nothing erased | `{"result": "memories=[MemoryEntry(content=Content(\n  parts=[\n    Part(\n      text='Conversation on 2026-11-13: Customer wanted the $9.99 CloudNest Storage charge posted 2026-11-01 disputed; the cus` |
| adk | run-1/r4-erase-open-tab-case-followup | r4e1-s3 | guard | r4: the erased trip is still in no memory store | `{"Reykjavik": ["adk_episodes.db", "adk_sessions.db"], "krona": ["adk_sessions.db"]}` |
| adk | run-1/r4-lockout-and-step-up | r4l-ttl-b | working | r4: a 25-minute-old step-up in the same chat does not authorise a channel change | `{"value": "sms", "as_of": "2026-11-13T10:25:00Z", "expires_at": null}` |
| adk | run-1/r4-lockout-and-step-up | r4l-tick | working | r4: ...and left no transcript | `2 transcripts: ['r4l-s1', 'r4l-s2']` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | prospective | r4: a reminder falling due while the erasure is pending is never sent | `1 messages` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | semantic | r4: no fact remains | `{"travel_notice": {"value": "Montreal", "as_of": "2026-11-12T10:00:00Z", "valid_until": "2026-11-18", "expires_at": "2026-11-19T00:00:00Z"}}` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | episodic | r4: no episode remains or is written by the fire | `2 episodes; purged 0` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | working | r4: no transcript remains or is written by the fire | `3 transcripts: ['followup-F-fba5617e-1', 'r4e2-cli', 'r4e2-s2']` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-due | guard | r4: the reminder note and the trip are in no memory store | `{"locker key": ["lg_store.db", "lg_checkpoints.db-wal"], "Montreal": ["lg_store.db", "lg_checkpoints.db-wal"]}` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-fire-next | prospective | r4: still no message to the erased customer | `1 messages` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-s3 | episodic | r4: resuming the erased session id brings nothing back | `Here's what my records show from earlier:  - A conversation on **Nov 12**: you asked for a reminder to return the **FitPulse locker key** on Nov 16 at 6pm New York time, and mentioned a **Montreal** t …` |
| langgraph | run-1/r4-erase-closed-tab-local-reminder | r4e2-s3 | episodic | r4: the new chat's episode holds nothing erased | `Conversation on 2026-11-12: Marco requested a Nov 16, 2026 6pm New York reminder to return the FitPulse locker key and a Montreal travel notice until Nov 18. Reminder scheduled (followup F-fba5617e) b …` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | semantic | r4: an erasure pending at fire time still runs: no fact remains | `{"travel_notice": {"value": "Reykjavik", "as_of": "2026-11-13T10:00:00Z", "valid_until": "2026-11-28", "expires_at": "2026-11-29T00:00:00Z"}}` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | episodic | r4: no episode remains, and the fired follow-up wrote none | `2 episodes; purged 0` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | working | r4: no transcript remains: not the open tab, not the follow-up's own session | `3 transcripts: ['followup-F-66ec5dae-1', 'r4e1-s1', 'r4e1-s2']` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-fire-1 | guard | r4: nothing she said is in any memory store | `{"Reykjavik": ["lg_store.db", "lg_checkpoints.db-wal"], "krona": ["lg_store.db", "lg_checkpoints.db-wal"]}` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-fire-2 | episodic | r4: still no episode after the retry window | `2 episodes; purged 0` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-fire-2 | working | r4: still no transcript after the retry window | `3 transcripts: ['followup-F-66ec5dae-1', 'r4e1-s1', 'r4e1-s2']` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-s3 | episodic | r4: nothing erased comes back in a later chat | `Here's what's on file for you right now:  - **Contact channel:** none set - so anything Kestrel sends you (case follow-ups, reminders) goes by secure message in the Kestrel app. - **Travel notice:** n …` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-s3 | episodic | r4: recall, if used, returns nothing erased | `{"memories": [{"at": "2026-11-13T10:04:00Z", "text": "Conversation on 2026-11-13: Customer asked to dispute a Nov 1 CloudNest Storage $9.99 charge (T-3002), saying the subscription was cancelled in Oc` |
| langgraph | run-1/r4-erase-open-tab-case-followup | r4e1-s3 | guard | r4: the erased trip is still in no memory store | `{"Reykjavik": ["lg_store.db", "lg_checkpoints.db-wal"], "krona": ["lg_store.db", "lg_checkpoints.db-wal"]}` |
| langgraph | run-1/r4-lockout-and-step-up | r4l-ttl-b | working | r4: a 25-minute-old step-up in the same chat does not authorise a channel change | `{"value": "sms", "as_of": "2026-11-13T10:25:00Z", "expires_at": null}` |
| langgraph | run-1/r4-lockout-and-step-up | r4l-tick | working | r4: ...and left no transcript | `2 transcripts: ['r4l-s1', 'r4l-s2']` |
