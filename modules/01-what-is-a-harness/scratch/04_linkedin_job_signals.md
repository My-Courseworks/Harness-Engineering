# LinkedIn job-posting signals (2026-10-26), via LinkedIn MCP

## Method notes

- **The location filter is ignored** (the account region is India). Putting the city in the keywords works.
- **The parser returns a job id for the first result only,** so details are pulled with narrow keyword searches.
- **Postings give domain signals,** not interview questions. Each one is noted with what the agent owns end to end.

## Postings read in full

### Airwallex: Senior AI Engineer, Singapore (job 4476649242, about 1 week old)

- **Agent:** "Kai", Airwallex's AI assistant, across "payments, accounts, transfers, cards, expenses, and other financial workflows".
- **Direction:** "advancing Kai from assistance to action and, ultimately, toward autonomous finance".
- **Hard constraint:** "AI systems are probabilistic, while moving money requires precision, permissions, auditability, deterministic controls, and regulatory compliance". The engineer helps "define where AI should reason and where financial infrastructure must remain deterministic".
- **Work spans:** "agent architecture, orchestration, context and knowledge systems, ontology, evaluation, governance, monitoring, and reliability".
- **Maps to:** the digital-wallet and UPI LLD problems → *an agentic finance OS for businesses*.

### Netomi: Agentic Engineer II/III, India remote (job 4458881383)

- **Product:** an agentic CX platform for Delta, United, MetLife and MGM.
- **The role emphasises:** "retries, timeouts, idempotency", "non-happy path handling".
- **Assessment:** support-adjacent, so a weak fit for this catalogue.

### PayPal: Staff Agentic AI Engineer, Singapore (job 4482899493, 3 days old)

- **Focus:** "building agentic commerce, agentic knowledge, and personalization solutions".
- **Stack:** LangGraph, Vertex AI, Bigtable.
- **Assessment:** thin on detail, but confirms agentic commerce as a hiring theme at a two-sided payment network.

### ByteDance: Procurement Agent Engineer, Dubai (job 4463841163, reposted 1 month ago)

- **What they build:** "an AI-native procurement platform … building Procurement Agents", plus "the underlying System AI Harness that lets agents plan, act, and deliver reliably".
- **The domain:** "long workflows, rich business rules, and real decision-making".
- **Required skills:** "idempotency, retries, rate limiting, eventual consistency"; "planning, tool use, memory, multi-step reasoning, orchestration".
- **Related roles (same Corporate Service System):** Global Travel agent and Workplace Service agent.
- **Maps to:** procurement and purchase-to-pay; corporate travel booking (the Hertz and airline LLD analog).

### TikTok: AI Agent Engineer, TikTok LIVE, Singapore (job 4475103251, 2 weeks old)

- **Agent:** a "Performance Analysis Agent" for live streaming at billions-of-users scale.
- **Capabilities:**
  - automatic inspection and minute-level attribution of anomalies;
  - auto-generated A/B experiment reports;
  - analysis of themes such as power use, smoothness and load speed;
  - shift-left review of performance in code review.
- **Platform:** moving APIs to an MCP service framework, with memory and evaluation iteration.
- **Related roles:** TikTok Shop SEA agent; Global E-commerce agents (Affiliate, Conversational AI, Supply Chain and Logistics).
- **Maps to:** the TikTok/YouTube LLD problem → *an agent that owns quality of experience for a streaming platform*.

### talabat: Applied AI Manager, Dubai (job 4478850376, 1 week old)

- **The team:** "Applied AI Tribe … 40+ AI products"; "shipping agentic AI systems at scale, with a harness-first philosophy".
- **Process:** "ensure evaluation pipelines, LLM observability, tooling, and infrastructure are in place before agent logic is built on top"; golden datasets; weekly eval jobs.
- **Use cases:** business automations, data enrichment, automated decision-making.
- **Maps to:** the Swiggy/DoorDash LLD problem.

### DoorDash: Senior MLE, New Verticals Agentic Foundations, SF (job 4476469980, 1 week old)

- **Agent:** the flagship "Ask grocery assistant", improved through an "eval harness-optimization loop" on "prompts, tools, skills, and context".
- **Engineering work:** SLM post-training to cut latency and cost, "agentic memory", "agent-compatible product representations".
- **Next agents:** "new agentic experiences for Merchants and Dashers".
- **Maps to:** the Instacart/DoorDash LLD problem → *a grocery-shopping agent that builds a cart* (substitutions, inventory, budget).

### Reddit: Senior SWE, Agentic Ads Experience, SF remote (job 4442738443, reposted 1 week ago)

- **Product:** advertiser-facing agents: "campaign assistants, creative and ad copy generation, one-click campaign creation, audience discovery, conversational analytics, and optimization recommendations".
- **Key ask:** "make the right architectural calls on … a single-shot LLM call, a workflow, a skill, a retrieval system, an agent loop, human review, or no AI at all".
- **Risk named:** "data isolation, permissioning, auditability, and policy compliance when AI systems take action on behalf of advertisers"; exposing other teams' services "to the platform's centralized agent(s)".
- **Maps to:** the Reddit/Instagram ads LLD problem → *an agent that runs an advertiser's campaign end to end*, spending real budget.

### Manus AI: Agent Harness Engineer, Singapore (job 4480908328, 1 week old)

- **The title is literally "Agent Harness Engineer"**, with responsibilities to "build core systems for the agent runtime and control layer, covering context, tools, execution, feedback and safety boundaries".
- **It owns:** "context and memory, model and tool orchestration, task planning and execution, tools and MCP integrations, and evaluation and quality feedback".
- **Preferred experience:** "execution isolation, least privilege, multi-tenancy, prompt-injection defenses, high-risk action approvals or auditing".
- **Use:** evidence that "harness engineering" is now a job title. It's a general agent rather than a domain, so it supports the course framing more than a catalogue entry.

### Carro: SWE, AI Agent Platforms & Distributed Systems, Singapore (job 4479146601, 1 week old)

- **Carro is a car marketplace;** the role is its enterprise agent orchestration platform.
- **It covers:** multi-tenant async runtime, stateful task graphs with "verification, and error recovery", model gateway failover, dynamic typed tool registries and sandboxes, WebSocket streaming with "connection recovery", and "multi-tier memory … global, session-scoped, and contextual state" with background memory consolidation.
- **Use:** an infrastructure signal; a weak domain signal.

## Takeaways from the LinkedIn sweep

1. **"Harness" is in the job titles and descriptions themselves:** ByteDance ("System AI Harness"), talabat ("harness-first"), Manus ("Agent Harness Engineer"), DoorDash ("eval harness-optimization loop").
2. **The domain agents that consumer companies are hiring for** map onto LLD problems:
   - Airwallex: autonomous finance (wallet / UPI)
   - PayPal and Replit: agentic commerce and payments
   - DoorDash: grocery cart agent (DoorDash / Instacart)
   - Reddit: advertiser campaign agent (Reddit / Instagram ads)
   - TikTok: streaming-performance agent and Shop agents (TikTok / YouTube)
   - ByteDance: procurement and corporate travel (Hertz / airline)
   - talabat: delivery-ops automation (Swiggy)
3. **The recurring constraints:**
   - "where AI should reason and where … infrastructure must remain deterministic" (Airwallex);
   - "actions on behalf of" a customer, with permissioning and audit (Reddit);
   - idempotency, retries and eventual consistency (ByteDance, Netomi, Manus).
4. **Location coverage:** Singapore and Dubai came through via keywords; the US via company-name searches. India results dominate when no location is given.

## Domain signals from result lists (title, company, city)

- **US:**
  - Replit: Staff SWE, Agentic Commerce & Payments; Staff SWE, Agentic Ads
  - OpenAI: SWE, ChatGPT Shopping (seen in results); Plugin Ecosystem; Cooperative AI
  - Ramp: Applied AI Engineer
  - American Express: FDE, Enterprise AI Platforms
  - Waymo: Senior Staff, Agentic AI Engineering
  - Uber: AI Solutions, Applied AI and GenAI staff roles
  - Square: GTM Systems & AI
  - Whatnot: AI Tooling
  - Eightfold: AI Agentic Product
  - LeanData: Staff Engineer, Agentic AI

- **Fintech and payments, Singapore:**
  - PayPal: Staff Agentic AI Engineer and Senior Agentic AI Engineer (job 4482899493)
  - Binance: Senior AI Agents Backend Engineer; AI Agent Engineer
  - Airwallex: Staff AI Engineer
  - Arta Finance: Backend / Systems Agentic Engineer
  - Partners Group: Forward Deployed Engineer
  - DBS, OCBC, UOB, SGX: AI engineers
- **Commerce and social, Singapore:**
  - TikTok: AI Agent Engineer, TikTok LIVE; AI Agent Algorithm Engineer, Global E-Commerce (Affiliate; Conversational AI)
  - Shopee: Chatbot Algorithm Engineer, Marketplace Intelligence
  - Agoda: Staff Software Engineer, GenAI
  - rednote: Agent / LLM Algorithm Engineer
  - Jump Trading: Research Engineer, AI Agents
- **Enterprise ops, Dubai:** ByteDance runs Corporate Service System agent roles for Global Travel, Procurement ("Procurement Agent Engineer") and Workplace Service.
- **Dubai, other:**
  - talabat: Applied AI Manager (food delivery)
  - Orient Insurance (Al-Futtaim): AI/ML Engineer
  - Azizi Developments and Danube Properties: AI automation (real estate)
  - MultiBank Group: AI Engineer (brokerage)
  - Fuse Energy: Applied AI Engineer
  - Deeplight AI: Applied AI Engineer, Agentic Systems
- **FDE roles, Singapore:** OpenAI (FDE, Deployment Lead FDE, Applied AI Engineer); Cognition (FDE APAC); Google Cloud (GenAI FDE, several); Meta (FDE Enterprise AI); AWS (FDE); Salesforce; SAP; LangChain; Exa; AssemblyAI (FDE Triage).
- **FDE and agent roles, San Francisco:**
  - FurtherAI (insurance)
  - Charta Health (healthcare)
  - Serval (IT ops agents)
  - Closr
  - Seso (agricultural labor)
  - Simple AI and Bland (voice agents)
  - Arize (FDE)

## Cut from the production-problems doc (2026-10-26)

The first draft re-skinned classic LLD products as agents (37 problems). The user rejected it: most collapsed into one shape, an agent acting for a person with an approval gate, where only the domain changes. Kept: 6 problems whose core difficulty is distinct. Cut, with the reason for each:

- **Same "act for a person, with approval" shape, in a new domain:** grocery cart; Swiggy-style agent surface; delivery ops; ride booking; seller ops; pricing; expense approval; accounts payable; group expenses; KYC onboarding; bank ops; catastrophe claims; insurance backbone; trip booking; corporate travel; car rental; ad campaign; recruiter; sales outreach; procurement on legacy ERP; tax prep; leasing office; parking operator.
- **Investigation archetype, already first-catalogue H2:** account-takeover investigation (Grab), AML (FIS), streaming quality (TikTok LIVE), the on-call agents.
- **Borderline, not added:**
  - Outbound voice agents negotiating with businesses (C.H. Robinson, HappyRobot): a variant of E4.
  - Agents driving legacy UIs with no API (Duvo, TaxGPT): a variant of first-catalogue E3.
  - Turning production traces into a cheaper fine-tuned model (Shopify's continual-learning loop, DoorDash's small-model post-training): overlaps first-catalogue G4.
- **Side notes kept here, not in the doc:**
  - "Harness" now appears in job titles (Manus's Agent Harness Engineer) and descriptions (ByteDance "System AI Harness", talabat "harness-first", DoorDash "eval harness-optimization loop").
  - The evidence upgrades for first-catalogue H2, B5, A5, A6 and D8 are listed in scratch 02 and 03.
