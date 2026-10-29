# ADK Delegation Patterns: AgentTool, Chat Sub-Agents and Task Sub-Agents

How an orchestrator hands work to other agents in Google ADK, what each mechanism does to control, context and state, and how to choose between them. Every claim is tagged by how it was established — see [Evidence and versions](#evidence-and-versions).

## Contents

- [Summary](#summary)
- [Evidence and versions](#evidence-and-versions)
- [The mechanisms](#the-mechanisms)
  - [AgentTool](#agenttool)
  - [Sub-agent in chat mode](#sub-agent-in-chat-mode)
  - [Sub-agent in task mode](#sub-agent-in-task-mode)
  - [Sub-agent in single-turn mode](#sub-agent-in-single-turn-mode)
- [What happens when no mode is set](#what-happens-when-no-mode-is-set)
- [Side-by-side comparison](#side-by-side-comparison)
- [Orchestrator configurations](#orchestrator-configurations)
  - [Unconfigured sub-agents](#unconfigured-sub-agents)
  - [Explicit chat sub-agents](#explicit-chat-sub-agents)
  - [Task sub-agents](#task-sub-agents)
  - [Mixing modes](#mixing-modes)
- [Use case examples](#use-case-examples)
  - [Example for AgentTool](#example-for-agenttool)
  - [Example for chat sub-agents](#example-for-chat-sub-agents)
  - [Example for task sub-agents](#example-for-task-sub-agents)
- [How to choose](#how-to-choose)
- [Caveats and open questions](#caveats-and-open-questions)
- [Relevance to this project](#relevance-to-this-project)
- [Sources](#sources)

---

## Summary

- **Three ways to delegate**, differing in who keeps control:
  - **`AgentTool`**: the specialist is called like a function. The caller keeps control and receives a result.
  - **Chat sub-agent** (`mode='chat'`, also the default): control is *transferred*. The sub-agent owns the conversation until something transfers it away.
  - **Task sub-agent** (`mode='task'`): the caller *delegates a bounded task*. The sub-agent may talk to the user to complete it, then returns a structured result and control comes back automatically.
- **Not configuring a mode is valid** and gives chat mode, so "unconfigured" and "`mode='chat'`" are the same thing.
- **The practical question is therefore chat versus task** (plus `AgentTool` for stateless utility calls):
  - Does the orchestrator need to stay in charge between steps? → task (or `AgentTool`).
  - Should a specialist take over the whole dialogue? → chat.
- `AgentTool` and task mode both return a result to the caller. They differ in session handling and in whether the specialist may talk to the user.

## Evidence and versions

Inspected: `google-adk 2.11.0`, the version installed in this project's `dspy` environment. Nothing below was run end to end; "verified in code" means read in the installed source.

| Tag used below | Meaning |
|---|---|
| **Code** | read in the installed `google-adk 2.11.0` source |
| **Docs** | stated in the official documentation or Google Cloud blog |
| **Unconfirmed** | seen in a search summary only, or inferred; treat as a hypothesis |

Where sources disagree, both are given (see [Caveats and open questions](#caveats-and-open-questions)).

## The mechanisms

### AgentTool

- **What it is:** an agent wrapped as a tool and added to the caller's `tools=[...]`. The caller's model calls it like any function. The sub-agent runs once and its answer comes back as the tool result.
- **Session handling (Code):**
  - It runs in a *separate runner with an in-memory session*, so its events do not become part of the caller's session history.
  - The caller's state is *copied in* (keys starting with `_adk` are filtered out), and any `state_delta` the sub-agent produces is *forwarded back* to the caller's state.
- **Who replies to the user:** the caller. The sub-agent's output is just data to it.
- **User interaction:** none. It is a single request and a single response.
- **Typical fit (Docs):** "discrete, stateless, and reusable capabilities" — the specialist that, given a request, returns an answer, with no need for the conversation.

### Sub-agent in chat mode

- **What it is:** an agent listed in the parent's `sub_agents=[...]` with `mode='chat'` or no mode.
- **How the parent reaches it (Code):** an automatic `transfer_to_agent` tool, plus instructions that list the available targets and their `description`s. The parent's model picks a target from those descriptions.
- **Who can be a transfer target (Code):** the agent's chat-mode sub-agents, its parent (unless `disallow_transfer_to_parent=True`), and its peers (unless `disallow_transfer_to_peers=True`). Sub-agents in `task` or `single_turn` mode are excluded.
- **After the transfer (Code):** the sub-agent replies to the user, in the same session, with full access to the history and state. The next user message goes to the agent that replied last, if that agent can transfer to others in the hierarchy; otherwise it goes to the root.
- **Getting control back:** a model-chosen transfer to the parent or a peer. Setting `disallow_transfer_to_parent=True` instead forces control back to the parent on the next turn, which prevents the user being stuck in a one-way transfer (Code, from the field's own documentation).
- **Typical fit (Docs):** specialists that own a whole interaction — "complex, stateful, and context-dependent processes".

### Sub-agent in task mode

- **What it is:** an agent in `sub_agents=[...]` with `mode='task'`, used for a bounded piece of work that may need user input.
- **How the parent reaches it (Code):** the parent gets a *tool named after the sub-agent*, not `transfer_to_agent`. The tool's declaration comes from the sub-agent's `input_schema` (a default is used when none is set) and carries the note not to call it in parallel with other tools.
- **How it ends (Code):** ADK adds a `finish_task` tool to the sub-agent. Calling it with a result (typed by `output_schema`, with a default wrapper otherwise) completes the task, and control returns to the parent automatically.
- **Context (Code):** events are *scoped* to the task. The task agent does not see the parent's conversation. Its first turn is built from the arguments of the originating function call ("your task is X"). The events still live in the parent's session, tagged with that scope.
- **User interaction (Docs):** allowed, for clarifying questions.
- **Not a transfer target (Code):** a task agent is never offered through `transfer_to_agent`.
- **Limits (Docs):** task agents must be leaf nodes (no sub-agents of their own). Task mode is documented as disabled for graph-based workflows in v2.0.0.

### Sub-agent in single-turn mode

- **What it is:** like task mode, but with no user interaction at all.
- **How the parent reaches it (Code):** a tool wrapper (`_SingleTurnAgentTool`), also excluded from transfer.
- **Parallelism (Docs):** designed to run in parallel for independent sub-tasks.
- **Typical fit:** independent lookups that need no clarification. It is not one of the three use cases below, but belongs in the mode list.

## What happens when no mode is set

- The `mode` field defaults to `None`.
- **Code:** when an `LlmAgent` is placed in a parent's `sub_agents`, ADK sets `mode='chat'` on it automatically. The source comment reads "LlmAgent sub-agents default to chat mode (unchanged behavior)".
- **Docs:** the field's documentation says the default is "chat as a sub-agent, single_turn as a node in a workflow".
- **Consequence:** `sub_agents=[a, b, c]` with no modes is the classic transfer setup, identical to setting `mode='chat'` on each.

## Side-by-side comparison

| | `AgentTool` | Sub-agent, chat (or unset) | Sub-agent, task |
|---|---|---|---|
| Parent reaches it through | its own tool, named after the agent | `transfer_to_agent` | a tool named after the agent |
| Who keeps control | the caller | the sub-agent, after transfer | the caller |
| Who replies to the user | the caller | the sub-agent | the sub-agent during the task, the caller at the end |
| Return of control | the tool call returns | a model-chosen transfer back | automatic, on `finish_task` |
| Talks to the user | no | yes | yes, for clarification |
| Conversation history seen | none (separate session) | all of it (shared session) | none (scoped to the task) |
| State | copied in, changes forwarded back | shared directly | shared |
| Events stored in caller's session | no | yes | yes (scoped) |
| Typed input and output | request in, text out | none | `input_schema` and `output_schema` |
| Parallel use | multiple tool calls possible | one active agent at a time | not parallel with other tools |

## Orchestrator configurations

### Unconfigured sub-agents

- `sub_agents=[...]` with no `mode` anywhere is the same as the next case: chat mode.

### Explicit chat sub-agents

- The orchestrator's model *transfers the conversation* to a specialist based on the specialists' descriptions.
- The specialist replies directly and stays the active agent for the next user message.
- The orchestrator is not involved between the user's turns, and it cannot post-process the specialist's answer.
- Multi-step workflows across specialists depend on each hop being chosen correctly by a model.
- Descriptions are the routing table: overlapping descriptions cause mis-routing.

### Task sub-agents

- The orchestrator *calls* each specialist for a defined piece of work and receives a structured result.
- It stays in charge between steps: it reads one result, decides the next call, and writes the final answer.
- Each specialist may ask the user questions mid-task, then finishes with `finish_task`.
- This suits fixed or conditional multi-step workflows where one step's output feeds the next.

### Mixing modes

- Modes are set per sub-agent, so one orchestrator can combine them: some specialists as `task`, one conversational specialist as `chat`, utility specialists as `AgentTool`s.
- Constraint (Docs): a task agent cannot have its own sub-agents.

## Use case examples

The three examples use three unrelated domains. Each is chosen for the single property that only its mechanism provides.

### Example for AgentTool

**Scenario: a data-analysis assistant that needs SQL written for it.**

- **Setup:** the analyst agent talks to the user and holds a tool that runs read-only queries. For writing the SQL, it calls a `sql_writer` agent exposed as an `AgentTool`.
- **Flow:**
  1. The user asks for the average order value by month.
  2. The analyst calls `sql_writer` with the question and the table schema.
  3. `sql_writer` returns a SQL string. It does not talk to the user.
  4. The analyst runs the query, reads the rows, and explains the result.
- **Why this mechanism:**
  - The request is self-contained: question plus schema in, SQL out. The specialist needs no conversation history.
  - There is nothing to clarify with the user.
  - The result is data the caller consumes programmatically, not something the user should see directly.
  - The same specialist can be reused by any other agent that needs SQL.
- **Property demonstrated:** a stateless, reusable specialist behind a function-call boundary.

### Example for chat sub-agents

**Scenario: a telecom support hotline with a front desk and three specialists.**

- **Setup:** a `front_desk` agent with chat-mode sub-agents `billing_support`, `technical_support` and `retention`, each described by what it owns.
- **Flow:**
  1. The user says "I was charged twice this month."
  2. `front_desk` transfers to `billing_support`.
  3. `billing_support` converses over many turns: it verifies the account, explains the charges and opens a dispute. The user's replies go straight to it.
  4. Later the user says "also, I want to cancel my plan." `billing_support` transfers to the `retention` peer, which takes over the conversation.
- **Why this mechanism:**
  - The specialist must own a long, open-ended dialogue.
  - The front desk has no work to do between turns.
  - The answer is the conversation itself, and nothing needs to flow back to a coordinator.
  - The specialist needs the whole history, which the shared session provides.
- **Property demonstrated:** the conversation changes hands, and the specialist stays active until it transfers away.

### Example for task sub-agents

**Scenario: a trip planner that assembles an itinerary from steps that each need a short exchange with the user.**

- **Setup:** a `trip_planner` orchestrator with task-mode sub-agents `flight_search` and `hotel_search`. Each declares an `output_schema`.
- **Flow:**
  1. The user asks for a trip to Lisbon in March.
  2. The planner calls `flight_search` with origin, destination and rough dates.
  3. `flight_search` asks the user: "Are your dates flexible? Do you want nonstop only?" It uses the answers, picks an option, and calls `finish_task` with `{flight_id, price, arrival_time}`.
  4. Control returns to the planner, which calls `hotel_search` with the arrival time and the remaining budget.
  5. `hotel_search` asks about location preference, finishes with its result, and the planner composes the itinerary.
- **Why this mechanism:**
  - Each step needs a short dialogue with the user, which `AgentTool` does not allow.
  - Each step returns a typed result that the planner must use in the next call, which a chat transfer does not guarantee.
  - The planner stays in control, so ordering and the budget check live in one place.
- **Property demonstrated:** a bounded task with user clarification, followed by an automatic structured return.

## How to choose

- **Does the specialist need to talk to the user?**
  - No → `AgentTool` (or `single_turn` if the work is independent and parallelizable).
  - Yes → chat or task; continue below.
- **Should the orchestrator stay in control and use the result?**
  - Yes → task.
  - No, the specialist should own the conversation → chat.
- **Does the specialist need the full conversation history?**
  - Yes → chat (task and `AgentTool` both start from a narrow input).
  - No → task or `AgentTool`.
- **Is the work a single discrete function with no state?** Plain function tools may suffice, and an agent may not be needed at all (Docs: tools are for "discrete, stateless, and reusable capabilities").
- **Is the process multi-step and stateful?** Sub-agents; Google's own example is a travel planner whose flight and hotel steps need "multiple back-and-forth interactions with the user".

## Caveats and open questions

- **Not run.** None of the modes was executed in this project. Behaviors are from reading the 2.11.0 source and the documentation.
- **State in `AgentTool`: sources disagree.**
  - The Google Cloud blog says agents-as-tools cannot access the caller's state.
  - The 2.11.0 source copies the caller's state into the sub-agent's temporary session and forwards state changes back.
  - Rely on the source for this installed version, and re-check when upgrading.
- **"AgentTool is discouraged in ADK 2.0" is unconfirmed.** It appeared in a search summary, and the page it pointed to did not mention AgentTool. The docs fetched do not say it either.
- **Task mode in graph workflows (Docs):** documented as disabled in ADK Python v2.0.0 for graph-based workflows, with re-enablement expected. Whether that restriction touches a plain `sub_agents` hierarchy on 2.11.0 is untested.
- **Chat-mode reliability:** transfers and hand-backs are chosen by a model from the sub-agents' descriptions, so mis-routing is possible. Clear, non-overlapping descriptions are required, and `disallow_transfer_to_parent` is the guard against one-way transfers.
- **Single parent:** an agent instance can belong to only one parent, so reusing a specialist under two parents needs separate instances (for example from a factory function).
- **Task tools are not parallel:** the generated tool description says not to call a task tool in parallel with other tools.

## Relevance to this project

- The operations desk in `../my_multi_agent/README.md` currently describes its domain agents as `AgentTool`s. That was an assumption, not a decision.
- The intended wiring is `Agent(..., sub_agents=[...], tools=[notify, current_date])`.
  - Domain agents that are part of multi-step workflows (for example onboarding: People, then IT, then Scheduling) fit **task mode**, because the orchestrator must stay in control and pass `emp_id` along.
  - A domain agent that should own a whole conversation fits **chat mode**.
  - Independent lookups fit **single-turn mode**.
- Open follow-up: update the multi-agent README's "Wiring" bullet and workflow section once the modes are chosen and tried.

## Sources

- [Where to use sub-agents versus agents as tools (Google Cloud blog)](https://cloud.google.com/blog/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools)
- [ADK collaboration modes (chat, task, single-turn)](https://adk.dev/workflows/collaboration/index.md)
- [Agent Development Kit: multi-agent applications (Google Developers Blog)](https://developers.googleblog.com/agent-development-kit-easy-to-build-multi-agent-applications/)
- [adk-python discussion on `transfer_to_agent`](https://github.com/google/adk-python/discussions/3330)
- [Nebius: multi-agent customer support walkthrough](https://nebius.com/blog/posts/build-multi-agent-ai-customer-support-system)
- Installed source, `google-adk 2.11.0`: `agents/llm_agent.py` (mode, transfer settings, sub-agent tool wrapping), `flows/llm_flows/extensions/_agent_transfer.py` (transfer targets), `tools/agent_tool.py` (`AgentTool`, task and single-turn wrappers), `agents/llm/task/_finish_task_tool.py`, `flows/llm_flows/context/_contents.py` (task scoping), `runners.py` (active-agent selection).
