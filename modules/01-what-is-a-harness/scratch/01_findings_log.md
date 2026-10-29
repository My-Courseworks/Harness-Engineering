# Scratch — agentic design interview research log (2026-10-26)

Working notes. Not the deliverable. Final report lives one level up.

## Lens carried over from the ops-desk critique

Problems worth cataloguing are the ones where the *harness* is the hard part, not the model:
- who enforces policy (tool code vs prompt)
- refuse-to-guess protocols (needs_input / needs_clarification)
- state as the only continuity for history-less sub-agents
- confirmation / HITL gates that can't be flipped by the model
- parallel fan-out racing on shared state
- clock / seed drift, two sources of truth
- idempotency of writes across restarts

## Sources read so far

### Aced (tryexponent.com/blog/* now 301 → aced.io)
- anthropic-system-design-interview — "multiple engineers" who did staff SWE/infra loop. Prompts: single-GPU batching (100/batch, sync users) = most common; e2e LLM batching; P2P file distribution; 100k rps token-gen; file cache; KV store; web crawler; **"Design an agentic AI system that can autonomously adapt to new tasks" (MLE roles)**. Eval: strip the AI framing to find the infra core; failure modes; staff = drive scope.
- openai-system-design-interview — Playground, Slack, job scheduler, streaming platform, chat app. Scale is the dominant axis; full-stack (UI + API + storage).
- ai-engineer-interview-questions — company-attributed:
  - Scale AI: insurance-claims agent → approval decision using RAG (token cost)
  - Sierra: customer-service agent for hypothetical outdoors company; agentic support for Spotify; AI agent for a streaming service; AI system integrating 3rd-party company data+workflows
  - Databricks: doc-processing pipeline for heterogeneous docs for LLM use
  - xAI: file uploader for AI chat app, large multimodal uploads into context
  - Anthropic: sampling API w/ batching & orchestration
  - OpenAI: GPU credit management; Playground
  - unattributed: real-time voice AI app

### techinterview.org
- agent-system-design-interview (2026-07-23): "plan and book a trip" = core prompt, "almost every AI-focused loop at Anthropic, OpenAI, Series A". Coding agent (read repo, run tests, open PR). Probes: tool loop, when to split agents (default "not yet"), double-charge after restart (idempotency), trajectory eval.
- ai-agent-infrastructure-interview (2026-05-04, upd 06-30): "infra platform for running AI agents at scale" (BYO agent code); variants: coding-agent platform (Cursor background agents / Claude Code), support infra 1M conv/day, research agent w/ 30+ min traces, safe arbitrary code exec. Probes: sandbox (Firecracker/gVisor), per-trace billing w/ unknown cost, mid-trace spend caps, replay, multi-tenant creds.

### Repos
- alirezadir/Agentic-AI-Systems — 06_interview_prep/genai-agentic-system-design.md; 04_use_cases: customer_support, document_processor, legal-doc-assistant, research_agents.

### Search-result-only (not yet fetched)
- KDnuggets: "Design GitHub Copilot", "Design an AI code reviewer"
- DesignGurus: Decagon SD interview — knowledge ingestion, ticket → answer → act
- Codemia: Amazon agentic AI engineer — refund-safe support agent, Bedrock tool agents
- Blind: Anthropic SD threads — ChatGPT-style w/ auth/sharing/history; distributed job queue w/ DLQ
- ByteByteGo GenAI SD book (Aminian & Sheng) — 10 case studies, chatbot/RAG/… no multi-agent

## Running problem list (raw, dedupe later)

### More sources read (second sweep)
- Cognition/Devin (techinterview 2026-07-05): "design the execution environment Devin runs inside"; probes: isolate untrusted code, <1s warm env, snapshot/branch/rollback, "agent runs for six hours", egress w/o secret exfil. Phone screen: reconcile state after failed step w/o double-applying side effect.
- Cursor (techinterview 2026-04-24): agent mode multi-file edits w/ verification + rollback; privacy-preserving inference for enterprise code; (tab prediction, training pipeline = non-agentic).
- Sierra (techinterview 2026-05-05): reasoning loop for enterprise support agent; tool orchestration w/ security boundaries (CRM, billing, KB); eval infra at enterprise scale. DesignGurus Sierra: "design an agent that handles subscription cancellation for a company".
- Replit (techinterview 2026-05-05): multi-tenant sandbox sub-second cold start; AI coding agents w/ tool use + reasoning loops.
- Decagon (DesignGurus, "candidates report"): help-articles → answers ingestion; AI gateway w/ audit, rate limits, logging, cost, tenant isolation; support agent reads ticket → acts (refund); eval & monitoring.
- Glean (techinterview 2026-07-20): 2 of 3 candidates got "design a search system over a company's documents" (permission-aware).
- Codemia Amazon (upd Sep 2026): refund-safe CS agent; "agent loops forever on failing tool call"; "developer agent that fixes failing builds"; multi vs single agent.
- KDnuggets (2026-08-19): ChatGPT, customer support AI, GitHub Copilot, AI code reviewer, legal document assistant.
- PromptLayer (hiring side, 2025-07-11): ticket drafting+escalation agent; multi-agent cited research report; code-reading improvement agent; take-homes: CSV→email campaigns, doc Q&A w/ citations multi-hop, Python code review agent.
- LLM Dojo / dev.to (270 public reports): OpenAI — multi-tenant RAG w/ latency+cost; internal-doc search agent w/ permissions+citations+abstain (also Google, Lyft); safe harness for tool-using agent + eval platform. Meta — code-review agent w/ deterministic tools; LLM coding assistant e2e; prevent coding agent leaking private code. Google — injection-robust PII-safe review summaries; agent plans + calls approved tools w/o bypassing deterministic controls. Anthropic — 500GB weights to 1000 GPUs.
- techinterview security (2026-08-06): refund agent up to $500 "where you'd stop it"; email agent exfil; "never reveal system prompt" insufficient; payments DB write access pushback; toy agent shell exec.
- alirezadir bank: support-ticket triage, reply drafting + escalation, multi-agent cited research, coding assistant, unified agent over email/calendar/docs/chat, guardrails for private tools, cross-conversation memory, 1M queries/day cost.
- Educative: smart parking agent, multi-agent medical diagnosis, personal assistant like OpenClaw.
- DesignGurus Grokking AI SD: five forms — known ML product, GenAI content, add AI to existing, agent that acts, critique/scale existing design (10x).

### Evidence of absence (be honest in report)
- Blind OpenAI SD thread (2024-06-26) and Anthropic SD thread (2025-02-01): no questions disclosed.
- 1point3acres Decagon SD thread: 403. Hello Interview: no agent breakdown found.
- No company publishes its own agentic question bank, except PromptLayer (hiring-side).
- SRE / on-call agent: zero interview reports found.

### Trend (primary) sources verified by fetch
- Anthropic Building effective agents 2024-12-19; multi-agent research 2025-06-13; writing tools 2025-09-11; context eng 2025-09-29; Claude Code sandboxing 2025-10-20; long-running harnesses 2025-11-26; demystifying evals 2026-01-09
- Cognition Don't Build Multi-Agents 2025-06-12 (Walden Yan)
- Google A2A 2025-04-09; OpenAI harness engineering 2026-02-11; Meta Rule of Two 2025-10-31; OWASP Agentic Top10 2025-12-09
- search-confirmed: Willison lethal trifecta 2025-06-16; Manus ctx eng 2025-07-18; OpenAI practical guide Apr 2025; OpenAI ACP 2025-09-29; Brave Comet 2025-08-20; Mem0 2025-04-28; τ-bench 2406.12045; MCP security best practices; Replit DB deletion Jul 2025; Moffatt v Air Canada 2024 BCCRT 149

## Consolidated catalogue → 41 problems in 8 families (A–H). See final report.
Follow-up probes above are the "spoilers" deliberately kept OUT of the report.
