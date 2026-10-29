# PR Reviewer: relevance and difficulty of each harness module (M4–M17)

One bullet per course module, for the C3 code-review design. The facts, numbers and mechanisms are taken from [harness-architecture.md](harness-architecture.md), including the SCIP + Bazel code graph (agentic ADR-015, harness ADR-016). The relevance and difficulty ratings are a judgment made on top of that document; the document itself does not rate its modules.

- **M4 · Context assembly and budgets.** *Relevance high, difficulty medium.* Each unit-review call gets a 40k-token input budget split into 10 capped slots, each with a named rule for what to drop when it overflows. The fixed 5k system-and-tools prefix is byte-identical across every unit, so it is cached. What goes around the diff now comes from the code graph:
  - definitions are resolved through `callees`, not by name;
  - call sites are ranked through `callers` (at most 5 per symbol, 15 per unit);
  - units are grouped by dependency cluster, so an API change and its updated caller usually share one reviewer's window.
- **M5 · Retrieval and grounding.** *Relevance high, difficulty low.* Grounding is exact. `check_anchor` drops any finding whose quoted code doesn't match the changed lines or whose evidence lines don't exist; it's a string comparison, no entailment model. Whether the cited code really is a bug is left to the verifier, which can now follow `callers` to find an upstream guard; a guard outside both windows remains a stated residual. "No finding" is a valid answer, and the clean-PR set penalises noise.
- **M6 · Instruction layer.** *Relevance medium, difficulty low.* A short versioned constitution plus team `SKILL.md` checklists. Because each agent node is single-turn, drift over a long session doesn't apply. M6's tests become invariance and position pairs, such as the same bug placed in the first versus the last hunk. Most of the precision lives in each skill's "do not flag" list.
- **M7 · Memory and state.** *Relevance high, difficulty high.* Four memory types now carry the design:
  - **Episodic:** the findings ledger, with a fingerprint built from the code, never the model's wording.
  - **Semantic:** team priors with time decay, and dismissal embeddings.
  - **Procedural:** promotion into skills, gated by threshold, approver and retraction.
  - **External: the code graph,** the main build cost.
    - It runs SCIP indexers for four languages over a 40M-line monorepo, plus the Bazel dependency graph.
    - It is stored in content-addressed Postgres tables (no graph database).
    - A base build runs hourly, and a per-PR overlay is built in the sandbox.
    - Its correctness has to be proved by a 200-symbol accuracy spot-check.

  Working memory is small (one pass, four keys).
- **M8 · Tool interfaces.** *Relevance medium, difficulty low.* Five read-only, credential-free repo tools over a mirror pinned at two commits. The status rules:
  - **Never mislead:** `repo_grep` on a missing path returns `not_found`, and `find_symbol` never returns an empty caller list when the graph is down.
  - **Precision:** every `find_symbol` row carries `exact` or `heuristic` precision.
  - **Truncation:** results say "showing X of Y".
  - **Freshness:** results state "index as of main@<sha>".

  No repo-tool error is retryable by the model. Per-agent tool budgets (12 and 4) are enforced in a `before_tool_callback`.
- **M9 · MCP and tool platforms.** *Relevance low, difficulty low.* Production uses no MCP. GitHub's official server is used only by a developer-tooling agent, which is read-only, filtered and has no write tools. The real platform work is supply chain:
  - analyzers are pinned by image digest, run in the sandbox, and need a false-positive baseline;
  - SCIP indexers are pinned the same way, and an upgrade must not regress the graph-accuracy spot-check.
- **M10 · Control flow.** *Relevance high, difficulty low–medium.* A deterministic `Workflow` with two forks:
  1. analyzers alongside the overlay build;
  2. `check_contracts` alongside context selection.

  It contains two bounded agent loops (the reviewer: 12 tool calls, 180 s, 20 LLM calls; the verifier: 4 calls, 60 s) and a one-shot reply classifier. Shadow mode is its own graph branch. The one trap found was that `max_llm_calls` is counted per invocation, so the 20-per-unit cap needs a counter keyed by branch, with 160 per pass as a backstop.
- **M11 · Multi-agent patterns.** *Relevance medium, difficulty low.* Code acts as supervisor over two pools of single-turn workers (8 reviewers, 10 verifiers) plus one classifier, all passing typed objects, never prose. The cross-unit loss from splitting a PR is now mitigated by graph grouping and `check_contracts`. The open question is whether the verifier earns its roughly 15% extra cost; its ADR stays Proposed until shadow mode shows +5 points of precision for at most 25% more cost.
- **M12 · Evaluation.** *Relevance highest, difficulty high.*
  - **Targets:** precision at publish ≥ 80%, recall on planted bugs ≥ 55%, ≤ 0.3 comments per clean PR, recall on mined history ≥ 25%, and cross-unit recall ≥ 75% (≥ 95% for signature breaks).
  - **Eight eval sets:** planted bugs (600 PRs), mined history (1,500 PRs), clean PRs (800), human-labelled findings (400, with labeller agreement checked), injection (120 PRs), invariance and position (45 pairs), per-skill tests, and the graph-accuracy spot-check (200 symbols).
  - **Measuring real impact:** a quarterly contamination guard, a 5% impact holdout, and per-rule action-rate tracking that demotes weak `check_contracts` rules.
  - **Biggest ongoing effort, in this assessment:** the labelling loop and building the mined set.
- **M13 · Reliability.** *Relevance medium, difficulty medium.*
  - **The queue:** webhook dedup, `SKIP LOCKED` workers with a per-PR advisory lock, a 60 s debounce, and superseding or aborting passes for stale commits.
  - **Publishing:** idempotent through the `finding_posts` key.
  - **Failures go down a ladder:** retry, then `FallbackModel` across providers, then per-unit degradation, then partial or deterministic-only output.
  - **Graph failures degrade gracefully:**
    - the store is down: tree-sitter plus `repo_grep`, and `check_contracts` is skipped;
    - a build failed: serve the last good build, labelled with its age;
    - an overlay target times out: it becomes heuristic.

  It never blocks a merge, which is what makes "safe fail" always available.
- **M14 · Security and injection.** *Relevance high, difficulty medium.* All three legs of the lethal trifecta are present by design: private code, author-controlled input, and a public comment. Each is shrunk:
  - **Reach:** the tools and graph cover only this repo at two commits.
  - **Output:** a sanitizer removes HTML, images, foreign links and mentions, and caps length.
  - **Secrets:** redacted before the model sees anything.
  - **Testing:** an injection suite that must pass in full.

  **A new threat is that overlay indexing can execute PR code.** Annotation processors, cgo, Bazel repository rules and install scripts all run code. So the overlay runs in the sandbox with no network and no secrets, and outside contributors get a tree-sitter-only overlay. Advisory-only output keeps injected text away from merge control.
- **M15 · Guardrails and governance.** *Relevance medium, difficulty low.* The bot may only comment, edit its own summary and post a check run that is always neutral. The publisher has three GitHub call paths, and a unit test asserts it can reach nothing else, because the token itself allows more. There's no human gate on posting, since a comment is reversible. Aggregate noise is the risk to govern, through budgets, kill switches and dismissal-rate alerts that move a team to shadow mode.
- **M16 · Observability and LLMOps.** *Relevance high, difficulty medium.*
  - **Traces:** one per pass, tagged with prompt version and policy hash, with gate decisions recorded as span events.
  - **Early warning:** a rising rate of dropped findings whose quote didn't match (`quote_mismatch`) is the first sign of a model or prompt regression.
  - **Code-graph health:** freshness lag (paging past 24 h), overlay build time, the share of `find_symbol` rows that are `exact`, and `check_contracts` action rate per rule.
  - **North-star metric:** action rate (comments acted on over comments posted), guarded by dismissal rate.
  - **Effort:** wiring outcome labels back from PR events, and keeping 30-day content traces redacted and access-restricted.
- **M17 · End-to-end design.** *Relevance medium, difficulty low as integration.* The layers meet at typed seams: snapshot, then analyzers alongside the overlay, then contracts alongside context selection, then review, gate, verify, rank and publish. The doc's build order is:
  1. the ledger and outcome derivation, run against human review comments as a baseline;
  2. the base code-graph build and its accuracy spot-check, which developers can use before any model runs;
  3. the reviewer in shadow mode;
  4. the gates;
  5. labelling and the eval sets;
  6. the verifier A/B test.

  So integration risk is small next to M12's ongoing evaluation work and M7's code-graph build.
