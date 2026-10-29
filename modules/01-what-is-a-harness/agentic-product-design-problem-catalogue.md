# Agentic Design Problems from Production Systems

> Agent design problems taken from systems companies have built, deployed or are hiring for (sweep of 2026-10-26). Each one is a problem statement only.
>
> **Admission bar:** a problem is listed only if its core difficulty differs from every other problem here and in the [first catalogue](agentic-system-design-problem-catalogue.md). Moving the same "agent acts for a person, with an approval gate" shape into a new domain does not count as a new problem.

**Badges:** 🏭 the company's own engineering write-up · 🤝 a named deployment, sourced from the vendor, a partner or trade press (numbers are self-reported).

Research notes, including everything considered and cut, are in [`scratch/02`](scratch/02_company_engineering_blogs.md), [`scratch/03`](scratch/03_openai_anthropic_practitioner.md) and [`scratch/04`](scratch/04_linkedin_job_signals.md).

---

## The problems

#### P1. A marketplace where agents negotiate with agents 🤝
*Staff*

> Design a marketplace where every buyer and seller can be represented by an AI agent that lists, negotiates and closes deals on their behalf, within limits the person sets. Different people's agents may run on different models.

- **Deployed as:**
  - **Anthropic's Project Deal.** 69 employees' agents closed 186 deals with no human sign-off, and people represented by the weaker model got worse deals without noticing [D1].
  - **Luminance's contract agent,** which "can react in real time to changes made by a counterparty's AI" [D2].

#### P2. Delegating spending authority to an agent 🤝
*Staff*

> A person wants an AI agent to buy things for them at merchants the agent finds on its own. Design how that person grants spending authority, and how the merchant, the payment network and the person's bank each verify it at payment time, including on a real-time rail where payments can't be reversed. Then design what happens when the person disputes a purchase.

- **Deployed as:**
  - **Stripe tokens for ChatGPT purchases,** "limited to a specific merchant and basket total" [D3].
  - **UPI Reserve Pay and UPI Circle** in the NPCI–Razorpay–OpenAI pilot [D4].
  - **Visa agent transactions live in Europe** with more than 30 issuers [D5].
  - **Mastercard Agentic Tokens** issued to specific agents [D6].
- **Why it's live:** AP2 mandates [P1], Visa's Trusted Agent Protocol [P2], and OpenAI handing checkout back to merchants in 2026 [D7].

#### P3. Enriching a 30-million-product catalogue, writing to production 🏭
*Senior → Staff*

> Your marketplace has 30 million products with missing or wrong attributes: size, dietary flags, compatibility. Design an agent system that finds evidence for each one, fills the attributes in, and writes them to the live catalogue that shoppers see.

- **Built as:** DoorDash TRACE. It enriched 31M SKUs and lifted checkout conversion by 0.48% [E1].

#### P4. Auditing a company's spend when the evidence doesn't fit in context 🏭
*Staff*

> Design an agent that audits all of a company's card spend in a single run: up to 1,000 expenses, each with receipts, history, calendar entries and policy text. Some violations only show up across many expenses. Some employees write expense memos meant to talk the agent into approving.

- **Built as:** Brex's audit agent.
  - Native tool loops overflowed at 1,000 expenses, and a bash workbench cut P90 tokens from about 3M to 600–700k [E2].
  - It is tested by planting fraud in synthetic timelines [E3].

#### P5. Running a team's ML experimentation for weeks 🏭
*Staff*

> Design an agent that runs an ML team's experimentation programme for weeks at a time. It proposes hypotheses, plans experiments, launches training jobs that take days, recovers from infrastructure failures, and carries what it learns into the next round, all within a GPU budget engineers approve up front.

- **Built as:** Meta's Ranking Engineer Agent. "REA uses a hibernate-and-wake mechanism". About 2× model accuracy over baseline across six models [E4].

---

## Sources

| ID | Source | Publisher | Date |
|---|---|---|---|
| E1 | [TRACE: agentic catalogue enrichment][E1] | DoorDash (arXiv) | 2026-08-21 |
| E2 | [Long-running agents need bash][E2] | Brex | 2026-07-06 |
| E3 | [Simulation testing for an AI audit agent][E3] | Brex | 2026-03-12 |
| E4 | [Ranking Engineer Agent (REA)][E4] | Meta | 2026-03-17 |
| D1 | [Project Deal][D1] | Anthropic | 2026-04-24 |
| D2 | [Luminance autonomous negotiation][D2] | IT Brief | 2026-03-12 |
| D3 | [Instant Checkout in ChatGPT][D3] | Stripe | 2025-09-29 |
| D4 | [UPI shopping in AI chatbots pilot][D4] | TechCrunch | 2025-10-09 |
| D5 | [Visa agentic commerce live across Europe][D5] | Visa | 2026-07-02 |
| D6 | [Mastercard Agent Pay in Singapore][D6] | AI News | 2026-03 |
| D7 | [Walmart Sparky and the Instant Checkout walk-back][D7] | Retail Dive | 2026-03-25 |
| P1 | [Agent Payments Protocol (AP2)][P1] | Google Cloud | 2025-09-17 |
| P2 | [Visa Trusted Agent Protocol][P2] | Visa | 2025-10-14 |

[E1]: https://arxiv.org/abs/2608.20844
[E2]: https://www.brex.com/journal/long-running-agents-need-bash
[E3]: https://www.brex.com/journal/articles/simulation-testing-ai-audit-agent
[E4]: https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/
[D1]: https://www.anthropic.com/features/project-deal
[D2]: https://itbrief.co.uk/story/luminance-opens-ai-contract-tool-with-clearer-reasoning
[D3]: https://stripe.com/newsroom/news/stripe-openai-instant-checkout
[D4]: https://techcrunch.com/2025/10/09/india-pilots-ai-chatbot-led-e-commerce-with-chatgpt-gemini-claude-in-the-mix
[D5]: https://www.mynewsdesk.com/uk/visa/pressreleases/visa-and-banks-across-europe-reach-the-next-phase-of-agentic-commerce-unlocking-secure-access-to-merchants-3457328
[D6]: https://www.artificialintelligence-news.com/news/mastercard-agentic-payments-singapore-dbs-uob/
[D7]: https://retaildive.com/news/walmart-sparky-chatgpt-instant-checkout/815647/
[P1]: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
[P2]: https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html
