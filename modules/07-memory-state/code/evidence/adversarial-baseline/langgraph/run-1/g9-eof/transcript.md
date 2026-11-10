# langgraph · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 1; stdout tail:_

```
Kestrel card-care (LangGraph) | customer=eli session=eof-s1 | 'exit' ends the session and writes its episode

[you]:   [tool] search_policy({"question": "What contact channels can Kestrel use to contact customers?"})

[assistant]: You can be contacted by **email**, **SMS (text message)**, or **secure message** (the inbox in the Kestrel app). If you haven't picked one, Kestrel defaults to secure message.

Note that setting or changing your contact channel requires identity verification (card's last 4 digits and billing ZIP). Want to choose one?

[you]:
```

_stderr tail:_

```
graph_agent/agent.py", line 404, in <module>
    main()
    ~~~~^^
  File "/Users/aprabhak/.treehouse/Harness-Engineering-a6701b/1/Harness-Engineering/modules/07-memory-state/code/langgraph_agent/agent.py", line 397, in main
    chat(args.var_dir, args.user, args.session, args.now)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/aprabhak/.treehouse/Harness-Engineering-a6701b/1/Harness-Engineering/modules/07-memory-state/code/langgraph_agent/agent.py", line 365, in chat
    text = input("\n[you]: ").strip()
           ~~~~~^^^^^^^^^^^^^
EOFError: EOF when reading a line
```

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | a chat that ends without 'exit' (EOF) still writes its episode | `0 episodes; purged 0` |

## eof-idle-close  ·  maintenance  ·  2026-11-24T12:00:00Z

_maintenance:_ `{"purged_episodes": []}`

| | memory type | check | evidence |
|---|---|---|---|
| **FAIL** | episodic | the idle-session sweep does not write the episode twice | `0 episodes; purged 0` |
