# Agent design solutions

Worked designs for four problems from the [agentic system design problem catalogue](../agentic-system-design-problem-catalogue.md). Each problem has two documents:

- **`agentic-architecture.md`**: the agents, their tools, state, composition, MCP servers, auth, skills. Written in the narrative style of the [ops-desk README](../code/my_multi_agent/README.md).
- **`harness-architecture.md`**: the harness around those agents, one section per course module M1–M17, plus a tradeoff ledger.

In each harness doc, the **M7 · Memory & State** section is organised by M7's seven memory types (working, external, episodic, semantic, procedural, parametric, prospective). Each type is weighted by how much the design depends on it. The types the design depends on most get a store and schema, write and read paths as code, failure modes, named tests and numbers. Types absent by design name the code that keeps them absent.

Both end with `## Appendix` → `### ADRs`, one H4 per decision, following [ADR_structure.md](../ADR_structure.md).

All four are built on **Google ADK 2.13.0**. Claims about ADK are tagged **Code** (an `ADK/...` path in the 2.13.0 source), **Docs**, or **Unverified**. To re-check a Code tag, get the same source with `pip download google-adk==2.13.0 --no-deps` and unzip the wheel; `ADK/` means its `google/adk/` folder.

## The four designs

| Problem | System | Shape | Agentic ADRs | Harness ADRs |
|---|---|---|---|---|
| [B1. Permission-aware enterprise search](B1-permission-aware-enterprise-search/) | **Ask**: answers from Drive, Confluence, Jira, GitHub, Slack | One `LlmAgent` with five tools; permission checks and citation checks are code | 14 | 14 |
| [B2. Multi-agent research with a cited report](B2-multi-agent-cited-research/) | **Research Desk**: 30–60 minute cited reports | A chat app starts a background `Workflow` job; parallel researchers record evidence; one writer; citations checked by code | 14 | 13 |
| [C3. Code-review agent](C3-code-review-agent/) | **PR Reviewer**: one large monorepo | A deterministic `Workflow` pipeline with three narrow single-turn agents inside it | 14 | 14 |
| [E4. Real-time voice agent](E4-realtime-voice-agent/) | **Front Desk**: phone line of a fictional 60-location dental group | One flat live agent on Gemini Live through `run_live`, plus one offline wrap-up agent after the call | 14 | 14 |

## How the four answered the same questions

| Question | B1 search | B2 research | C3 code review | E4 voice |
|---|---|---|---|---|
| **Multi-agent?** | No: one agent | Yes, for reading only: parallel researchers, single writer | Narrow agents inside a code pipeline | No: one live agent, one offline agent |
| **`AgentTool` / transfer / `mode="task"`** | Compared and rejected | `AgentTool` and an LLM lead agent rejected; task-mode nodes noted as valid in 2.13 | Rejected; `parallel_worker` used instead | Rejected: a live-mode transfer reconnects after a 1.0 s sleep |
| **VFS-style flat orchestrator** | Kept as a principle; browsable tree rejected (listings leak hidden items) | Fits the evidence ledger only | Five read-only repo tools in VFS style | The "one flat orchestrator" idea fits; no VFS navigation |
| **MCP servers** | Vendor servers, read-only, called from inside tool code | Glean MCP for internal sources; web search through own tools over Exa and Brave | GitHub MCP for developer tooling only | None in the call path |
| **Auth** | Two permission checks: copied permissions, then a live check at the source; per-user OAuth only for Slack and live Jira | OAuth for Glean on the user's behalf | GitHub App tokens, one repo, one hour at most; no user OAuth | A caller-identity ladder; no OAuth |
| **`LongRunningFunctionTool`** | No: the slowest operation is a 2 s fan-out | Rejected for the job: it would leave a call unanswered in the chat for 45 minutes | No: the wrong tool for "wait for CI, then review" | No: slow reads are `NON_BLOCKING` tools with `WHEN_IDLE` scheduling |
| **A2A** | No, with a trigger to revisit | No in v1; says when it would matter | No | No |
| **Skills** | No | Research playbooks for the planner | Yes: per-language and per-team `SKILL.md` checklists, up to 3 per unit | Compiled into the instruction at build time |

## Findings that affect existing course material

These came up while checking the designs against the ADK 2.13.0 source. The first three I re-checked myself.

1. **`AgentTool` is discouraged.** Its docstring says to set `mode='single_turn'` on the sub-agent instead (`ADK/tools/agent_tool.py:123-132`). The ops desk's `AgentTool` wiring uses the discouraged form.
2. **`SequentialAgent`, `ParallelAgent` and `LoopAgent` are deprecated** in favor of `Workflow`, which cannot yet be a sub-agent of an `LlmAgent` (`ADK/agents/sequential_agent.py:88`, `parallel_agent.py:172`, `loop_agent.py:59`).
3. **`RoutedLlm` / `RoutedAgent`, cited in M11 and M13, don't exist in 2.13.** The nearest equivalent is `FallbackModel` (`ADK/models/_fallback_model.py:207`).
4. **M11 says task mode is disabled in graph workflows.** B2 reports that this matches the v2.0.0 docs but not the 2.13 source, which accepts task-mode nodes. I did not re-check this one.
