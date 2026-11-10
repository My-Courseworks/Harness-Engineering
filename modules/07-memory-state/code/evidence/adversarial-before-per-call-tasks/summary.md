# Evidence summary: adversarial-before-per-call-tasks

Pass counts per memory type, summed over every recorded live run.

| memory type | adk (1 runs) | langgraph (4 runs) |
|---|---|---|
| working | 4/4 | 12/16 |
| semantic | 1/1 | 2/4 |
| episodic | - | - |
| procedural | - | - |
| external | 1/1 | 0/4 |
| parametric | - | - |
| prospective | - | - |
| guard | 1/1 | 4/4 |
| **all** | **7/7** | **18/28** |

## Every failed check

| framework | where | step | memory type | check | evidence |
|---|---|---|---|---|---|
| langgraph | run-1/g64-otp-send-and-wait-in-one-response | sw-entry | external | the customer's entry two minutes later does not send a second code | `["Your Kestrel verification code is 222273. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 114636. It expires in 5 minutes. Kestrel will never as …` |
| langgraph | run-2/g64-otp-send-and-wait-in-one-response | sw-entry | external | the customer's entry two minutes later does not send a second code | `["Your Kestrel verification code is 203562. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 460619. It expires in 5 minutes. Kestrel will never as …` |
| langgraph | run-2/g64-otp-send-and-wait-in-one-response | sw-entry | working | the code they typed is the code that is checked: no failed attempt | `1 attempt rows with succeeded=0` |
| langgraph | run-2/g64-otp-send-and-wait-in-one-response | sw-entry | working | one code, consumed | `challenges: [('cancelled', '2026-11-12T10:00'), ('open', '2026-11-12T10:02')]` |
| langgraph | run-2/g64-otp-send-and-wait-in-one-response | sw-entry | semantic | and the channel is changed | `{}` |
| langgraph | run-3/g64-otp-send-and-wait-in-one-response | sw-entry | external | the customer's entry two minutes later does not send a second code | `["Your Kestrel verification code is 816970. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 327900. It expires in 5 minutes. Kestrel will never as …` |
| langgraph | run-4/g64-otp-send-and-wait-in-one-response | sw-entry | external | the customer's entry two minutes later does not send a second code | `["Your Kestrel verification code is 254725. It expires in 5 minutes. Kestrel will never ask you to share it.", "Your Kestrel verification code is 374021. It expires in 5 minutes. Kestrel will never as …` |
| langgraph | run-4/g64-otp-send-and-wait-in-one-response | sw-entry | working | the code they typed is the code that is checked: no failed attempt | `1 attempt rows with succeeded=0` |
| langgraph | run-4/g64-otp-send-and-wait-in-one-response | sw-entry | working | one code, consumed | `challenges: [('cancelled', '2026-11-12T10:00'), ('open', '2026-11-12T10:02')]` |
| langgraph | run-4/g64-otp-send-and-wait-in-one-response | sw-entry | semantic | and the channel is changed | `{}` |
