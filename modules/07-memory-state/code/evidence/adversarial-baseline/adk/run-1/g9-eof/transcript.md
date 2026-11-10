# adk · adversarial · run 1 · g9-eof

Live run against DeepSeek: every customer line below went to the real agent (simulated-customer lines were written live by the model playing the persona). Tool results are clipped.

## eof-s1  ·  cli_eof_session  ·  eli  ·  2026-11-24T10:00:00Z

_CLI exit code 1; stdout tail:_

```
Kestrel card-care (ADK) | customer=eli session=eof-s1 | 'exit' ends the session and writes its episode

[you]:   [tool] search_policy({"question": "What contact channels can Kestrel use to contact a customer?"})

[assistant]: Kestrel can reach you by **email**, **SMS (text)**, or **secure message** (the inbox in the Kestrel app). If you haven't chosen a channel, we default to secure message.

You currently have no channel on file, so secure message is in effect. Want to switch? Changing the channel requires identity verification — your card's last 4 digits and billing ZIP.

[you]:
```

_stderr tail:_

```
await asyncio.to_thread(input, "\n[you]: ")).strip()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/asyncio/threads.py", line 25, in to_thread
    return await loop.run_in_executor(None, func_call)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/concurrent/futures/thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)
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
