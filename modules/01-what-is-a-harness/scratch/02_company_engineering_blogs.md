# 02 — Company engineering blogs: agentic systems that run a workflow inside a product

Sweep date: 2026-10-26. Every system below was verified by fetching the cited page: the page itself, the publisher's RSS/Atom feed (full post body), or the company's own research page. Search snippets alone were not used. Where a page was behind a bot wall and could not be fetched, it is listed under "Could not verify" at the end, not as a system.

How to read the blocks: **Agentic quote** is verbatim and 25 words or fewer. **HITL** = human-in-the-loop points. "Not stated" means the post does not say.

Count: 20 qualifying systems (mobility 5, food & delivery 3, commerce 2, fintech & payments 4, social & content 3, hiring & professional 2, other 1, travel & rental 0, real estate 0).

---

## Mobility (Uber, Grab, Gojek)

### 1. Uber — Agent Mesh for on-call (Oncall / Investigation / Monitoring agents) + agent identity
- **Date / URL:** 2026-05-21 — https://www.uber.com/us/en/blog/solving-the-agent-identity-crisis/
- **Authors:** Matt Mathew, Prasad Borole, Meng Huang (with Sergey Burykin, Gaurav Goel, Bayard Walsh)
- **Agentic quote:** "Delegation is the default mode - agents work on behalf of others"
- **End to end:** An on-call engineer starts a session on an alert. The Oncall Agent delegates to an Investigation Agent, which reads logs, metrics and alerts and concludes the alert is misconfigured. It then hands off to a Monitoring Agent, which opens a pull request to change the alert threshold (CI runs on it). Tool calls go through an MCP Gateway that applies tool-level policy and redaction.
- **Writes to:** Source control (the PR). Observability systems are read-only.
- **HITL:** A human starts the session. No approval gate is described for the current agents; dynamic HITL access control is listed as future work.
- **Scale:** "Thousands" of internal agents adopted the identity system. One task can involve dozens of tool calls and delegations. Token-exchange P99 is under 40 ms (most under 10 ms).
- **Hard constraints:** Delegated identity across hops: SPIFFE/SPIRE workload identity, plus short-lived single-hop JWTs from a token-exchange service (RFC 8693) that carry an **actor chain** (user → Oncall → Investigation). Audits break if the originating user is lost mid-chain. Per-hop token exchange adds up as latency. Existing agents had to migrate to a standard A2A client.

### 2. Uber — Finch, conversational finance data agent
- **Date / URL:** 2025-07-17 — https://www.uber.com/us/en/blog/unlocking-financial-insights-with-finch/
- **Authors:** Eddie Huang, Taya Yusuf, Tim Ross (Uber FinTech)
- **Agentic quote:** "The Supervisor Agent receives the query and sends it to an appropriate sub-agent, such as the SQL Writer Agent."
- **End to end:** A finance user asks a question in Slack ("Q4 2024 GBs", then "compare to Q4 2023"). A LangGraph supervisor routes it to a SQL Writer sub-agent, which looks up column and value aliases in an OpenSearch metadata index, writes SQL and runs it on Presto / IBM Planning Analytics / Oracle EPM. It rewrites the query when it errors and streams status back to Slack.
- **Writes to:** Slack replies and Google Sheets exports. Nothing is written to source financial systems.
- **HITL:** None today. A roadmap item would send a leader's answer to an expert for verification.
- **Scale:** Not stated beyond "within seconds".
- **Hard constraints:** RBAC on financial dimensions, with the user's permission checked before any query runs. Hallucinated numbers matter here because executives decide on them. Getting WHERE-clause filters right needed fuzzy alias matching. Data sources disagree on which one is current.

### 3. Grab — SOP-driven agent for RiskOps account-takeover (ATO) investigations
- **Date / URL:** 2025-05-08 — https://engineering.grab.com/streamlining-riskops-with-sop (framework: 2025-04-25, https://engineering.grab.com/introducing-the-sop-drive-llm-agent-framework)
- **Authors:** Fujiao Liu, Haitao Bao, Jia Chen, Meichen Lu, Muqi Li
- **Agentic quote:** "The SOP planner serves as the navigator, guiding the investigation's path"
- **End to end:** Input is an ATO case. An analyst-written SOP (indented natural language compiled to JSON) defines each investigative step, the SQL it needs, external function calls (e.g. `@IP_web_login_history`) and the decision criteria. A planner walks the SOP tree depth-first. A worker agent runs the queries and calls and stores the results, and the agent picks the next branch. At the end it writes a decision and an investigation report (Slack integration is shown).
- **HITL:** Not described in the post.
- **Scale:** Handling time per ticket fell from 22 to 3 minutes. 87% of ATO cases have been automated. The post claims a "zero-error rate" but gives no method.
- **Hard constraints:** Fraud decisions must be reliable and auditable. Evidence is spread across many systems. The SOP is the control surface: the LLM fills gaps but does not invent the procedure.

### 4. Grab — multi-agent system for Analytics Data Warehouse requests (data + on-call + enhancement)
- **Date / URL:** 2026-03-19 — https://engineering.grab.com/from-firefighting-to-building
- **Authors:** Sneh Agrawal, Rishi Raj, Ayan Chatterjee, Wen Zhong Tan, Sai Reddy Kakumanu
- **Agentic quote:** "Agent analyzes requirements and gathers context through interactive dialogue with the engineer."
- **End to end:** Requests arrive from Slack and JIRA. A classifier routes them. Investigation questions go to Data, Code Search and On-call agents (Trino/Hive/Delta, GitLab, Airflow, Hubble catalog, Genchi data quality, Lighthouse monitoring), and a summarizer merges their findings. Enhancement requests go to an Enhancement Agent that gathers context, writes code and schema-change scripts, runs tests on Airflow, and opens GitLab merge requests.
- **Writes to:** GitLab MRs, Airflow test runs, Slack (answers labelled "unreviewed"), an annotation DB, and Postgres/Redis for state.
- **HITL:** Every MR is reviewed and merged by an engineer; nothing reaches production without approval. Reviewers can approve, reject, refine, re-route or annotate answers.
- **Scale:** Over 1,000 monthly users and more than 15,000 tables. Before this, the team spent about 40% of its time on repetitive requests.
- **Hard constraints:** Accuracy was chosen over latency for the sequential agents. Context grows across agents and needs pruning. More than 30 tools slowed the agents until the set was trimmed. PII checks, blocks on destructive SQL, and timeouts.

### 5. Gojek — multi-agent observability "AI brain" for alert triage
- **Date / URL:** 2026-04-27 — https://medium.com/gojekengineering/how-we-built-an-ai-brain-for-our-observability-stack-at-gojek-11a288e578bb (read via the publication's RSS feed)
- **Author:** Shivangi Parashar
- **Agentic quote:** "autonomously investigates across Prometheus metrics, Loki logs, Tempo traces, Kubernetes cluster state, and deployment history — simultaneously, in parallel"
- **End to end:** A Grafana webhook sends an alert to a LangGraph state machine. A context node resolves the owning team and its datasource UIDs from the service registry. An LLM router picks agents and whether to run them in parallel. Six read-only agents (PromQL, LogQL, TraceQL, K8s, deploy platform, VM/DMS) query through five MCP servers. A correlation agent synthesizes an RCA, and a "sufficient context" validator loops back to the router when evidence is thin. The RCA goes to Lark, with progress streamed over SSE.
- **Writes to:** Lark messages and persisted run metadata. "No agent takes action on production."
- **HITL:** Humans own escalation and remediation.
- **Scale:** More than 50,000 alerts a day, 40+ teams, 500+ microservices. Single-agent runs take about 4 s, parallel multi-agent about 8 s, sequential about 14 s. The re-route loop fires on 8% of runs. Generated queries are validated against live Prometheus, which catches bad label assumptions on 20–30% of queries.
- **Hard constraints:** The LLM invents metric names and labels, so retrieval is grounded in a 22k-document metric schema, enriched with live label values, and every matcher is validated after generation. Token cost: query generation alone was 40% of tokens.

---

## Food and delivery (Uber Eats, Instacart, DoorDash)

### 6. Uber Eats — Cart Assistant (agentic grocery cart building)
- **Date / URL:** 2026-06-16 — https://www.uber.com/us/en/blog/uber-cart-assistant/
- **Authors:** Anurag Biyani, Deepak Kumar Sahoo, Renato Beserra Sousa
- **Agentic quote:** "LLMs handle ambiguity; deterministic systems handle retrieval, pricing, eligibility"
- **End to end:** Input is a text prompt or a photo (handwritten list, recipe screenshot). An LLM plans items (search terms, quantities, constraints). Catalog and search APIs return candidates with availability, price, deals and sellable units. An LLM rubric judges relevance (direct match, variant, acceptable substitute, adjacent). Deterministic optimization enforces item- and cart-level price limits and eligibility. Quantities are converted to purchasable units with LLM reasoning plus arithmetic. Schema and scope guardrails run, an aggregator assembles a **draft cart**, and an LLM writes the shopper-facing text.
- **Writes to:** The user's draft cart. It does not place orders.
- **HITL:** The shopper reviews and edits the cart and checks out.
- **Scale:** Not stated.
- **Hard constraints:** Items are processed concurrently, so latency is set by the slowest item. Price caps must hold against live prices and promotions. Store-level inventory. Converting "2 lbs" into sellable units. Substitution text must be faithful to the products actually chosen.

### 7. Instacart — Blueberry, Slack-native on-call reasoning harness
- **Date / URL:** 2026-07-14 — https://tech.instacart.com/blueberry-force-multiplier-for-the-on-call-engineer-98c446dfcc12 (read via the tech.instacart.com RSS feed)
- **Authors:** Karthik Halukurike, Gabe de Oliveira, Hassan Jallad, Alan Wong
- **Agentic quote:** "let Blueberry decide when to call tools, fan out to sub-agents, deepen into evidence, or stop and respond"
- **End to end:** Ingress picks which Slack thread events earn a diagnostic pass: alerts, @mentions, DMs, follow-ups. Passes go on a **Postgres-backed durable queue** with parallel workers that can take over from each other. A processor loads the owning team's profile, skills and team-hosted MCPs on top of a shared baseline. The agent loop fans out sub-agents (postmortems, runbooks, prior incidents, deploys, flags, dependencies, anomaly sweeps) and posts a grounded explanation back in the thread. Every pass persists a session snapshot and a reasoning trace.
- **Writes to:** Slack threads and the persisted traces. A policy-gated **deploy-failure mitigation** path (redeploy, escalate or stop) is in testing. It requires preconditions, an action plan, plan reflection, an execution-policy check and result reflection.
- **HITL:** Engineers drive theory-testing follow-ups. Actions stay policy-gated.
- **Scale:** About 25k diagnostic passes a month across 270+ channels: about 17k auto-triages and about 7k engineer follow-ups. Time to first insight and time to test a theory both average about 3 min. 99.9% success rate, about 58k MCP tool dispatches, about 60 team profiles. In one cluster failure (90 P1/P2 alerts in 3 minutes) it ran more than 50 investigations in parallel.
- **Hard constraints:** It must survive worker restarts at 3 a.m. (durable state). Alert storms. Team specialization without forking the harness. Historical priors must inform but not override live evidence.

### 8. DoorDash — TRACE, agentic catalog enrichment that writes to the catalog
- **Date / URL:** 2026-08-21 — https://arxiv.org/abs/2608.20844 (a DoorDash, Inc. paper on arXiv, not a blog post; affiliation confirmed in the HTML version)
- **Authors:** Rohan Kumar, Steven Xu, Kyle MacDonald, Matthew Long, Bernice Chow, Mac VanRenterghem, Sudeep Das
- **Agentic quote:** "decides whether to publish it or route it to human review"
- **End to end:** A ScoutAgent gathers multimodal evidence (merchant catalog, syndicated feeds, images, identity-matched web search) and proposes attribute values with supporting evidence, abstaining when the evidence conflicts. A JudgeAgent re-checks each value under a stricter policy and can run its own searches, returning PASS / FAIL / UNVERIFIED / UNCERTAIN. A write gate then routes each value to WRITE, BLOCK or REVIEW.
- **Writes to:** The production catalog.
- **HITL:** UNCERTAIN values go to human review. The review rate is not reported.
- **Scale:** 31M SKUs enriched across four verticals. Impression-weighted coverage rose 90.4%. Showing enriched attributes lifted checkout conversion by 0.48%. Offline accuracy was 98.2% at 74.7% coverage. Each SKU costs one Scout call and one Judge call.
- **Hard constraints:** Wrong attributes reach the product page, so publication is gated by evidence. Model cost multiplies across SKUs (the paper compares cost per model).

---

## Commerce (Shopify, Amazon)

### 9. Shopify — Sidekick (merchant admin agent), including Flow-automation generation
- **Date / URLs:** 2025-08-26 — https://shopify.engineering/building-production-ready-agentic-systems ; 2026-04-22 (updated) — https://shopify.engineering/fine-tuning-agent-shopify-flow ; 2026-08-05 — https://shopify.engineering/sidekicks-continual-learning-loop
- **Authors:** Andrew McNamara (with Ben Lafferty, Michael Garner) ; Ted Chaiwachirasak et al. ; Andrew McNamara, Cody Mazza-Anthony
- **Agentic quote:** "fill in optimized content directly into the product form"
- **End to end:** A merchant asks in natural language inside the Shopify admin. Sidekick queries store data through Admin GraphQL, builds customer-segment filters, writes content such as SEO descriptions into product forms, and navigates the admin. For automations, a fine-tuned Qwen3-32B agent calls `task_search` to get trigger/action summaries and `task_configuration` to get full schemas for just 2–3 of them. It writes the workflow as Python, which a transpiler converts to Flow's JSON DSL. The result is a **Shopify Flow** workflow the merchant then activates.
- **Writes to:** Product forms, segments, and Flow workflows in the merchant's store.
- **HITL:** Success is measured by whether merchants activate the generated workflow. None of the three posts describes an explicit approval step before mutations.
- **Scale:** Millions of merchants. The GraphQL agent handles up to 2,000 requests per minute. The Flow model serves most production Flow traffic, 2.2x faster and 68% cheaper than the frontier model it replaced. The continual-learning loop cut estimated serving cost from about $27M a year to about $1M (−96%).
- **Hard constraints:** Tool sprawl ("death by a thousand instructions"), handled with just-in-time instructions. Reward hacking in GRPO: the model opted out of hard tasks and hallucinated IDs and enums. At 1% traffic the fine-tuned Flow model showed a 35% activation gap that offline benchmarks had missed. Silent infrastructure regressions took days to trace.

### 10. Amazon — Insight Agents for sellers (Seller Central data and insight agent)
- **Date / URL:** 2025 (SIGIR 2025) — https://www.amazon.science/publications/insight-agents-an-llm-based-multi-agent-system-for-data
- **Authors:** Jincheng Bai, Zhenyu Zhang, Jennifer Zhang, Jason Zhu
- **Agentic quote:** "IA has been launched for Amazon sellers in US, which has achieved high accuracy of 89.5% based on human evaluation"
- **End to end:** A seller asks a business question. A manager agent screens out-of-domain queries (lightweight encoder-decoder) and routes the rest (BERT classifier). A data-presentation worker breaks the query into parts and calls internal APIs to build the data model. An insight-generation worker produces insights, with domain knowledge injected.
- **Writes to:** Read-only; it returns answers to the seller.
- **HITL:** Not stated.
- **Scale:** US launch. 89.5% human-judged accuracy. P90 latency under 15 s.
- **Hard constraints:** Low latency on a seller-facing surface. Coverage across many seller data APIs. Accuracy for business decisions. The page is a paper abstract, so detail is thin.

---

## Fintech and payments (Ramp, Brex, Monzo)

### 11. Ramp — Policy Agent (autonomous expense approval)
- **Date / URL:** 2025-07-10 — https://builders.ramp.com/post/how-to-build-agents-users-can-trust
- **Authors:** CJ Enright, Will Koh, Felix Zhang
- **Agentic quote:** "we've seen more than 65% of approvals be fully handled by the agent"
- **End to end:** The customer's expense-policy PDF is ingested and kept in an in-product editor. For each expense, the relevant policy sections go to the LLM. Output is one of three states, **Approve / Reject / Needs review**, with a rationale that cites the policy sections. Deterministic hard stops (dollar limits, vendor blocklists, category rules) run alongside. The workflow builder defines where and when the agent may act.
- **Writes to:** Approval decisions in Ramp's expense workflow.
- **HITL:** An **autonomy slider** (e.g. review everything over $50, or only what the agent flags). Rollout goes suggestions → act on subsets → full autonomy. Uncertain cases fall back to the existing escalation path.
- **Scale:** More than 65% of approvals handled fully by the agent.
- **Hard constraints:** LLM confidence scores are unreliable, hence categorical outputs. Finance users lose trust fast. User actions are lenient ground truth (finance teams approve slightly out-of-policy spend), so golden sets are reviewed. Ambiguous policy language confuses both the model and humans.

### 12. Brex — Audit agent (spend review, abuse and fraud detection)
- **Date / URLs:** 2026-07-06 — https://www.brex.com/journal/long-running-agents-need-bash ; 2026-03-12 — https://www.brex.com/journal/articles/simulation-testing-ai-audit-agent
- **Authors:** Hercules Gimenes, Sai Chiligireddy (bash post); the simulation post's author bio names Rohit (an AI engineer), no surname shown
- **Agentic quote:** "We cannot prescribe every investigation path upfront. The agent has to decide what to inspect, join, discard, and carry forward."
- **End to end:** Per expense or batch, the agent inspects receipts, user history, prior cases, calendar context, web research and policy text. It then takes a **financial action**: approve, reject, flag for review, request more information, or send a policy reminder. The goal is review-by-exception. The runtime moved from native tools to a bash workbench (`just-bash`, a virtual filesystem inside Node). Domain commands such as `get_expenses`, `analyze_receipt`, `get_cases`, `web_search` and `submit_review` are composed with pipes and files, so raw artifacts stay out of the model context.
- **Writes to:** Review outcomes and cases on Brex spend.
- **HITL:** The highest-value actions are escalated to finance teams.
- **Scale:** Reviews spend in real time. After the runtime change, P90 tokens per run fell from peaks near 3M to about 600–700k, and P95 run time roughly halved. The benchmark ran at 10 / 100 / 1,000 expenses.
- **Hard constraints:** At 1,000 expenses native-tool loops overflowed context and lost recall ("Low recall loses the case"). Adversarial memos with fabricated policy citations try to talk the agent into approval. Fraud labels are scarce, so testing uses seeded **simulation**: archetypes, mutations that plant known violations, a 90-day synthetic timeline, and precision/recall graded per violation type.

### 13. Brex — AI-native multi-agent KYC and underwriting onboarding
- **Date / URL:** 2026-01-20 — https://www.brex.com/journal/rebuilding-onboarding-ai-native
- **Author:** "Building Brex" (company byline)
- **Agentic quote:** "When confidence falls below a defined threshold (e.g., when data sources conflict) the case is escalated to a human analyst."
- **End to end:** A business application arrives. Segmentation agents (LinkedIn via Clay, company website) estimate whether the applicant is professionally invested. OCR and verification agents check proof of address, articles of incorporation, SAFEs and bank statements. Identity and fraud agents look at behavioral signals, with a fuzzy-match agent for name mismatches. Underwriting agents map the applicant to underwriting segment policies. A **decision agent** combines claims, evidence and confidence with Brex policy and approves instantly or escalates. Agents exchange structured claims, evidence and confidence.
- **Writes to:** Onboarding approve/reject decisions and requests for information (RFIs).
- **HITL:** Low-confidence or conflicting cases go to analysts, and their decisions feed back as supervised signals.
- **Scale:** Onboarding went from days to minutes. Card-application auto-approval went from 0% to 40% in weeks. Manual identity reviews fell 70% and business-address RFIs fell 85%.
- **Hard constraints:** Regulated KYC and underwriting. Every decision needs a reasoning trail. **Repeatability**: the same application must give the same outcome. Agents must be able to say "not sure". Governance must be built into the system, not bolted on.

### 14. Monzo — Ops Agent (regulated bank operations workflows)
- **Date / URL:** 2026-06-04 — https://monzo.com/blog/engineering-the-future-of-customer-operations-the-monzo-ops-agent
- **Authors:** Jamie McDonald-Gibson, Joost van Oorschot, Robin Dhamankar, Tom Leitch
- **Agentic quote:** "The agent is no longer only deciding what to say; it is learning how to execute operational workflows."
- **End to end:** A customer chat comes in and is classified into one of more than 150 intents. Customer context such as transactions is gated by intent. The agent reads account data through tools and runs defined operational workflows, such as finding a missing refund or ordering replacement cards for fraud victims and lost or broken cards. Other actions named include reporting fraud and setting up direct debits; card blocking is used as the example of a state-changing tool call in testing. A triage step decides whether to respond, hand off or close.
- **Writes to:** Account state (card replacement, fraud reports, direct debits).
- **HITL:** Input and output guardrails hand off to human specialists. At launch a human reviewed every outgoing message. QA sampling started at 100% and decreases over time.
- **Scale:** More than 150 intents, aiming at hundreds. Intent-gated context improved resolution on transaction queries by 10 percentage points.
- **Hard constraints:** Heavy regulation means reliability and measurability come first. Conversations are long and non-linear, so evaluation uses LLM-simulated users and simulated tool environments. A fix in one component moves failures elsewhere. This entry clears the support-chatbot exclusion because the agent takes consequential, regulated actions on accounts.

---

## Social and content (Spotify, Meta, Pinterest)

### 15. Spotify — Ads AI, multi-agent media-plan builder for advertisers
- **Date / URL:** 2026-02-19 — https://engineering.atspotify.com/2026/2/our-multi-agent-architecture-for-smarter-advertising
- **Authors:** Pratik Rasam, Ralph Sylvain
- **Agentic quote:** "The LLM reasons about what to do; tools provide accurate data to work with."
- **End to end:** An advertiser describes a campaign in 1–3 messages. A RouterAgent decides which resolvers to run: goal → objective, audience (interest taxonomy, geo/age/gender), budget ("5k" → micro-units), schedule (relative dates). The resolvers run in parallel and call geo lookup, ad-category search and historical-performance services. A MediaPlannerAgent then scores ad-set candidates against historical campaign performance. Built on Google ADK and Vertex AI.
- **Writes to:** Media-plan recommendations. The post does not say it creates campaigns in the ad server.
- **HITL:** The advertiser refines the plan conversationally.
- **Scale:** A media plan takes 5–10 s instead of 15–30 min. 20+ form fields become 1–3 messages. Responses take about 3–5 s. The number of recommendations scales with budget (1 under €1k, 4–5 above €15k).
- **Hard constraints:** Output must be reliably parseable (strict guardrails and a parsing layer). Choosing agent boundaries: too many agents add latency, too few produce a monolithic prompt. Responses are synchronous, with streaming left for later.

### 16. Meta — Ranking Engineer Agent (REA), autonomous ads-ranking experimentation
- **Date / URL:** 2026-03-17 — https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/
- **Authors:** Ashwin Kumar, Erwin Gao, Matan Levi, Sheela Yadawad, Sherman Wong, Sneha Iyer, Vinodh Kumar Sunkara
- **Agentic quote:** "REA uses a hibernate-and-wake mechanism."
- **End to end:** A hypothesis generator, working with a research agent and an engineer, proposes ideas from a historical experiment-insight DB. The REA Planner writes a multiphase plan (Validation → Combination → Exploitation). The REA Executor launches training jobs through schedulers, hibernates while they run, and wakes when results are ready. It debugs infrastructure failures from a runbook and drops jobs that hit OOM or loss explosions. An experiment logger writes outcomes back to the insight DB.
- **Writes to:** Training-job schedulers, experiment tracking, and the insight DB.
- **HITL:** Engineers approve the plan and the **GPU cost estimate** up front, review preflight access checklists, and make the final launch decisions.
- **Scale:** About 2x average model accuracy over baseline across six models. Three engineers delivered proposals for eight models (previously about two engineers per model).
- **Hard constraints:** Jobs run for hours to days and workflows for weeks (persistent state, hibernate and wake). Compute budgets are enforced by pausing or halting at thresholds. Access is scoped to the ads-ranking codebase. Routine failures are handled without escalating.

### 17. Pinterest — Analytics Agent (text-to-SQL with execution)
- **Date / URL:** 2026-03-06 — https://medium.com/pinterest-engineering/unified-context-intent-embeddings-for-scalable-text-to-sql-793635e60aac (read via RSS; predecessor 2024-04-02 "How we built Text-to-SQL at Pinterest")
- **Authors:** Keqiang Li, Bin Yang
- **Agentic quote:** "An LLM with Pinterest-specific prompts classifies tasks … and decides which tools to call and in what order."
- **End to end:** An analyst asks in natural language. An orchestration LLM picks among doc lookup, table discovery, query discovery, text-to-SQL and execution. MCP tools cover table search (vector DB + PinCat), query-pattern search (query history embedded by analytical intent), knowledge search, and **Presto execution with EXPLAIN-before-EXECUTE**, tight LIMITs and error-recovery loops. SQL may reference only existing columns and reuses validated join keys and filters. Ranking is governance-aware: tier, freshness and documentation quality.
- **Writes to:** Executes read queries. Separately, LLM-drafted table documentation is written into PinCat and marked as AI-generated.
- **HITL:** Humans review docs for Tier-1 tables. Output relies on EXPLAIN validation plus human review.
- **Scale:** More than 100k tables and 2,500+ analytics users. It reached 40% of analysts within two months and is the #1 agent at Pinterest, with 10x the usage of the next one.
- **Hard constraints:** Only specific join patterns are correct among many plausible tables. Filter values must match the actual data ("WEB" vs "web"). The table footprint had to be cut from about 400k to about 100k before the agent could work.

---

## Hiring and professional (LinkedIn)

### 18. LinkedIn — Hiring Assistant (sourcing → evaluation → outreach → screening)
- **Date / URL:** 2025-10-21 — https://www.linkedin.com/blog/engineering/ai/how-we-engineered-linkedins-hiring-assistant
- **Authors:** Xiaoyang Gu, Xie Lu, Daniel Hewlett
- **Agentic quote:** "its lifecycle is orchestrated entirely through asynchronous message passing"
- **End to end:** A recruiter states intent in chat. A supervisor runs a plan-and-execute loop over sub-agents. The intake agent refines requirements and generates qualifications. The sourcing agent iteratively refines Recruiter Search and Recommended Matches queries over 1.2B+ profiles. The evaluation agent scores candidates with evidence, using fine-tuned models with speculative decoding. The outreach agent sends messages and follow-ups and answers candidate questions. The screening agent prepares questions and transcribes and summarizes screens. A learning agent personalizes, and cognitive memory is scoped to each recruiter. It runs on headless versions of Recruiter tools, with background jobs and daily pipeline refreshes.
- **Writes to:** Candidate pipelines and projects, InMail and outreach, phone-screen scheduling, recruiter memory, notifications.
- **HITL:** The recruiter approves qualifications before evaluation starts and makes the final advance decisions. Changes the learning agent proposes need approval. The supervisor routes critical actions for human approval, and the recruiter can take over screening at any time.
- **Scale:** 1.2B+ profiles. Background jobs over millions of profiles. Candidates evaluated in seconds.
- **Hard constraints:** Real-time chat on top of long-running async jobs, synced across devices. One agent instance per recruiter, with private memory that is never used across customers or for training. Cost and latency drove per-task model choice. Messages to candidates go out under the recruiter's name.

### 19. LinkedIn — SQL Bot (internal data-analyst agent)
- **Date / URL:** 2024-12-09 — https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics
- **Authors:** Albert Chen + 17 co-authors
- **Agentic quote:** "SQL Bot is a multi-agent system built on top of LangChain and LangGraph."
- **End to end:** Intent routing (find tables, answer dataset questions, write SQL, and so on). Embedding retrieval returns 20 tables; an LLM re-ranks them to 7 and then selects fields. A planner solves the question step by step. Validators check existence and run EXPLAIN, and a self-correction agent repairs errors and can fetch more tables. Users run the query in DARWIN, which has a "Fix with AI" button.
- **Writes to:** Read-only SQL. Execution stays in the user's notebook.
- **HITL:** An optional guided mode lets users pick tables at each step. Feedback and follow-ups.
- **Scale:** Millions of tables, pruned to a few thousand. Hundreds of users. Integrating into DARWIN raised adoption 5–10x. "Fix with AI" accounts for about 80% of sessions.
- **Hard constraints:** **Per-dataset ACLs**: if the user lacks direct access but a group they belong to has it, the bot emits code that uses the group's credentials. Table churn and deprecation. Implicit team context (what "CTR" means differs by team). Many questions have more than one valid answer.

---

## Travel and rental

No qualifying engineering post found. See the "Checked, nothing qualifying" list: Booking.com, Expedia, Airbnb, MakeMyTrip, Agoda, Hertz/Avis, airlines, hotels.

## Real estate

No qualifying engineering post found (Zillow: job postings and an interview only).

## Other (enterprise workflow inside a consumer company)

### 20. Uber — Legal Redlining Agent (contract negotiation inside Word)
- **Date / URL:** 2026-10-08 — https://www.uber.com/us/en/blog/building-ubers-redlining-agent/
- **Authors:** Austin Greco, Meghana Somasundara, Frank Tenente
- **Agentic quote:** "When a MODIFY decision is reached, we reference historical feedback and rules to refine the clause."
- **End to end:** Inputs are a counterparty-redlined Word contract, the source contract, playbooks, a database of lawyer-authored rules, and a store of past lawyer decisions. The agent separates external redlines from Uber's own, detects the counterparty's intent and assesses risk, with policy lookup running in parallel. A deterministic rules engine overrides the model on a strict rule match. Otherwise it retrieves similar past decisions (about 20 candidates, with time-decay weighting and a 365-day half-life) and decides **accept / reject / modify**. It drafts compromise language and counterparty comments, applies a tone pass, and applies the changes in Word through the Office JS API.
- **Writes to:** The Word document (tracked changes and comments), the feedback and rules indexes, and Redis session state.
- **HITL:** A lawyer accepts, rejects or edits every suggestion before it goes back to the counterparty, and those decisions feed the learning loop.
- **Scale:** Thousands of contracts a year. Average review time down more than 20%. 91% decision accuracy.
- **Hard constraints:** The Office JS API is slow, crashes on some structures and returns empty strings for deleted tracked text, so the agent keeps its own text state. Tone swung between too defensive and too accommodating, and legal experts now own the tone prompt. Legal positions drift over time (time-weighted retrieval).

---

## Borderline or excluded after reading (verified, but not counted)

- **Monzo — Fraud Prevent agent** (2026-07-27, https://monzo.com/blog/combining-generative-ai-and-predictive-modelling-to-fight-financial-crime). It sits in the live payment path: a risky payment is paused, the customer answers a questionnaire, and a multimodal LLM extracts structured features that a supervised model scores. In practice it is one LLM step, not a multi-step agent. The post states "we do not ask the LLM to decide whether a payment is fraudulent". Worth knowing as a counter-pattern.
- **Meta — Thin Orchestrator for data-column onboarding** (2026-10-19, https://engineering.fb.com/2026/10/19/ml-applications/thin-orchestrator-ai-agent-architecture/). A 1,300-line deterministic router sends 20+ workflows to 14 specialist sub-agents through workflow templates. Config prep dropped from 3–4 days to under an hour, and about two-thirds of changes land without major human edits. Excluded because the output is code changes across three repos (a coding agent), but the architecture lesson is strong.
- **Razorpay — AI security triage** (2026-06-09, engineering.razorpay.com via RSS). L1 triage of SAST findings uses 29 sub-skills; L2 generates remediation PRs. Excluded as coding-adjacent.
- **Shopify — Catalog clustering** (2026-06-17, https://shopify.engineering/catalog-clustering). A two-stage LLM propose-then-critique pipeline assigns unified product IDs across billions of products. The post itself calls it a fixed pipeline, not an agent.
- **Zalando — Content Creation Copilot** (2024-09-18). One GPT-4o call per article pre-fills attributes for copywriters; about 50k attributes a week at about 75% accuracy. Not agentic.
- **Intuit — Intuit Assist AR/AP and cash-flow agents** (2025-02-20, https://www.intuit.com/blog/innovative-thinking/delivering-done-for-you/). Drafts invoices and reminders for user review; customers get paid 5 days faster. Product-level post with no engineering detail.
- **Mercari — IBIS incident buddy** (2025-02-06). RAG over past postmortems. RAG-only, so excluded.
- **Lyft — ARIA analytics assistant** (2026-07-09). The post covers building the frontend during onboarding; the agent itself is not described.
- **Expedia — Romie** (2024-05-14). A product announcement (group-chat trip planning, disruption alerts) with no engineering detail. The 2026 Expedia posts are about operating models and governance.

## Could not verify (bot wall or no fetchable first-party source)

- **DoorDash engineering blog** (careersatdoordash.com): "Building Ask DoorDash" Parts 2–6, including the grocery-reorder case study and the agent platform with an Orchestrator → domain agents over A2A and MCP, plus "Beyond Single Agents". Every fetch returned a Cloudflare 403, including the RSS feed. Search snippets claim a reorder path cut from about 16 s to about 2 s. **Not verified.** This is probably the single most relevant consumer food-ordering agent, so it is worth reading manually.
- **Coinbase** "Building enterprise AI agents at Coinbase" (institutional support, onramp onboarding, listing legal review): Cloudflare 403. Not verified.
- **Swiggy** MCP agentic ordering (4 MCP servers, 66 tools across Food, Instamart and Dineout): news coverage only; no Swiggy Bytes post found, and the feed did not resolve.
- **Instacart Cart Assistant** and the ChatGPT checkout integration: news coverage and a company announcement only; no tech-blog post found.
- **PhonePe** merchant payment-gateway integration agent: press release only (not fetched).
- **Walmart "Marty"** supplier/advertiser super-agent: news coverage only.
- **Stripe** Smart Disputes and dispute auto-resolve, and LLM-assisted onboarding (80%+ auto-clear): product pages and Sessions talks only, not engineering posts; not fetched.
- **Airbnb** trust-and-safety agents: known only from a third-party talk summary.
- **Booking.com** AI Trip Planner and itinerary agent: conference abstracts only.

---

## Companies checked with nothing qualifying

Lyft, Airbnb, Booking.com, Expedia, Agoda, MakeMyTrip, Etsy (LLM extraction and search posts, not agents), eBay (no tech-blog post found), Zalando (copilot is a single LLM call; the Agentic Identity Broker is infrastructure), Reddit (Snoocode is coding; CSAM detection), Quora/Poe (nothing found), YouTube/Google (nothing found), Netflix (nothing found), TikTok/ByteDance (nothing found), Duolingo (its own posts describe a human-plus-AI content pipeline, not agents), Stripe, PayPal (agent-toolkit and MCP announcements only), Revolut, Nubank (enablement and workshop post only), PhonePe, Paytm, Razorpay (excluded, see above), Flipkart (threat-intel LLM), Meesho, Zillow, Coinbase (blocked), Intuit (product-level only), Mercari (IBIS is RAG; the PM agent is Claude Code skills), Rakuten (vendor case studies only), Delivery Hero (job postings only), Zomato, Swiggy (news only), Walmart, Mercado Libre (secondary sources only), Hertz/Avis, airlines (vendor marketing only), hotel chains (Marriott and Hilton job posts and news only).

---

## Cross-cutting patterns

1. **Deterministic shell, LLM core.** The systems that work put the LLM only where ambiguity lives and keep everything with money or correctness at stake deterministic: price caps and cart building (Uber Cart Assistant), hard policy stops (Ramp), rules-engine override (Uber Redlining), SOP trees (Grab), a thin deterministic router (Meta). The design question is less "which agent framework" and more "where exactly is the LLM allowed to decide."

2. **Categorical, abstaining outputs instead of confidence scores.** Ramp (Approve / Reject / Needs review), DoorDash TRACE (WRITE / BLOCK / REVIEW), Brex onboarding ("agents must be able to say they're not sure") and Monzo (respond / hand off / close). The abstain path is the HITL design. Its calibration, meaning how often the agent defers, is a product metric.

3. **Graduated autonomy as a rollout mechanism.** Ramp's autonomy slider, Monzo's 100% QA review stepping down, Instacart's policy-gated mitigation path, LinkedIn's approve-before-evaluate step. Teams treat autonomy as a dial per tenant or per action class, not a launch-day switch.

4. **Long-running and asynchronous work is the hard infrastructure problem.** LinkedIn's async message passing and background jobs, Meta REA's hibernate and wake over days, Instacart's Postgres durable queue with takeover. A chat-shaped request/response loop does not hold up; these systems need durable state, resumability and progress streaming (Gojek's SSE).

5. **Context is the bottleneck before the model is.** Brex moved from native tools to a bash workbench because tool results flooded the context (P90 tokens 3M → 600–700k). Shopify uses just-in-time instructions and a summary-then-detail tool pair. Grab trimmed 30+ tools. Gojek capped labels in context. Recall collapses at scale when raw data passes through the transcript.

6. **Identity and permission for delegated agents is unsolved infrastructure.** Uber built actor-chain JWTs (user → agent → sub-agent), LinkedIn emits code using group credentials for ACL'd datasets, Finch checks the user's RBAC before every query, and Zalando's broker (excluded above) grants the intersection of user and agent permissions. The recurring interview question is "on whose authority does this tool call run, and can you audit it later?"

7. **Grounding against live system state, not just retrieval.** Gojek validates every PromQL matcher against live Prometheus. Pinterest runs EXPLAIN before EXECUTE and checks filter values against column profiles. Uber Cart Assistant re-checks live price and inventory. Teams found RAG over stale schema indexes isn't enough; the agent has to probe the real system before acting.

8. **Writes to production are rare and gated; most "agents" stop at a draft.** Uber Cart Assistant stops at a draft cart, Spotify at a recommended plan, Grab at a merge request, Uber Redlining at suggestions a lawyer approves. The systems that truly write (DoorDash TRACE to the catalog, Brex and Ramp decisions, Monzo account actions, Shopify Flow workflows) each have an explicit write gate. Reversibility decides where the gate goes: a draft cart is free to undo, a card replacement is not.

9. **Evaluation needs simulators because production labels are biased.** Brex plants fraud in seeded synthetic timelines because historical fraud labels are rare and skewed. Monzo uses LLM-simulated customers and simulated tools. Shopify has a merchant simulator and calibrated judges, and found a 35% activation gap only in a 1% live test. Ramp found user approvals too lenient to use as ground truth. Offline benchmarks repeatedly missed what live traffic exposed.

10. **On-call and internal data-analyst agents dominate the published record; consumer transaction agents are under-documented.** There are 5+ incident agents and 4 text-to-SQL agents, but almost no first-party engineering detail on agents that book trips, place orders or settle disputes. The consumer-booking stories (DoorDash, Swiggy, Instacart, Expedia, Booking) exist mostly as product news or behind bot walls. For a catalogue of interview problems, the "Uber/DoorDash/Hertz as an agent" problems will need constraints extrapolated from the fintech entries (Ramp, Brex, Monzo), which are the best-documented consequential-action systems.
