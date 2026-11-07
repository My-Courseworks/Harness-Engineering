"""Measure retrieval: local embeddings against keyword search, on the policy KB and on an episode history.

    python eval_retrieval.py      # writes evidence/retrieval/results.md

No model calls. Keyword search is SQLite FTS5 with BM25 and OR-joined query tokens, which is
what ADK's built-in SqliteMemoryService does; embeddings are the fastembed model both agents use.
Each labelled query has one correct document; recall comes with a Wilson 95% interval, because 12-15
queries are few. The distractor test adds near-miss episodes (same merchant, same city, same kind of
request, but the wrong conversation) and asks whether the right episode still ranks first. Questions the
KB cannot answer are scored separately: whether the best score separates "answerable" from "not in the KB".
"""

import math
import re
import sqlite3
from pathlib import Path
from statistics import mean

from cardcare.retrieval import POLICY_DIR, embed_texts, top_matches

CODE_DIR = Path(__file__).resolve().parent

POLICY_QUERIES = [
    ("How many days do I have to dispute something?", "dispute-window"),
    ("Is there a deadline for contesting a charge?", "dispute-window"),
    ("I got charged again after I cancelled my gym", "cancelled-subscriptions"),
    ("A streaming service billed me after I quit it", "cancelled-subscriptions"),
    ("What happens after I dispute a subscription charge?", "cancelled-subscriptions"),
    ("What does it cost to buy things in euros?", "foreign-transaction-fees"),
    ("Do you charge extra when I shop abroad?", "foreign-transaction-fees"),
    ("Does a travel notice waive the FX fee?", "foreign-transaction-fees"),
    ("Will my card work in Japan?", "travel-notices"),
    ("I'm going overseas, do I need to tell you?", "travel-notices"),
    ("Can you text me instead of emailing?", "contact-preferences"),
    ("How do you get in touch about my case?", "contact-preferences"),
    ("I lost my wallet", "card-replacement"),
    ("My card snapped in half", "card-replacement"),
    ("How long until a new card arrives?", "card-replacement"),
]
UNANSWERABLE_QUERIES = ["What's your late payment fee?", "What APR do you charge on purchases?",
                        "Can I raise my credit limit?", "Do you have a rewards programme?"]

EPISODES = [
    ("streammax", "Conversation on 2026-11-09: Priya disputed the StreamMax Premium charge T-1002 ($15.99) as a cancelled subscription; case C-5001 opened."),
    ("rejection", "Scheduled follow-up on 2026-11-19 (customer not present): told by SMS that case C-5001 was rejected, NO_CANCELLATION_PROOF."),
    ("lisbon", "Conversation on 2026-11-09: Priya set a travel notice for Lisbon until 2026-11-30 and asked about euro charges."),
    ("sms", "Conversation on 2026-11-12: Priya switched her contact channel from email to SMS after verifying her identity."),
    ("porto-reminder", "Conversation on 2026-11-20: Priya asked for a reminder on 2026-11-29 to set up a travel notice for Porto."),
    ("fx", "Conversation on 2026-11-09: Priya asked the foreign transaction fee on her purchases; told 1.25% of the dollar amount."),
    ("replacement", "Conversation on 2026-10-02: Priya reported a damaged card; a replacement ships in 5 business days."),
    ("bakery", "Conversation on 2026-11-10: Priya asked about a Pastelaria Lisboa charge of EUR 4.20; it was a valid purchase."),
    ("coffee", "Conversation on 2026-10-31: Priya checked a Bluebottle Coffee charge of $6.50; no action taken."),
    ("limit", "Conversation on 2026-09-15: Priya asked whether her credit limit could be raised; the assistant could not help with that."),
]
# Near misses for the distractor test: each one shares the topic of a labelled episode but is the wrong answer.
DISTRACTORS = [
    ("x-streamflix", "Conversation on 2026-08-14: Priya asked how to cancel a StreamFlix free trial; nothing was disputed."),
    ("x-lisbon-old", "Conversation on 2026-05-02: Priya asked whether her old Lisbon travel notice from spring had expired."),
    ("x-email", "Conversation on 2026-10-20: Priya asked whether emails from Kestrel were genuine; no preference changed."),
    ("x-reminder-paid", "Conversation on 2026-10-25: Priya asked for a reminder to pay her bill before the due date."),
    ("x-fx-refund", "Conversation on 2026-10-11: Priya asked why a euro refund posted for less than the purchase."),
    ("x-card-lost", "Conversation on 2026-07-19: Priya asked how to freeze her card while she looked for it; she found it."),
    ("x-cafe", "Conversation on 2026-09-03: Priya asked about a Cafe Lisboa tip that looked doubled; it was a pending hold."),
    ("x-dispute-other", "Conversation on 2026-09-28: Priya asked how long a dispute review usually takes, in general."),
]
EPISODE_QUERIES = [
    ("that streaming thing I had trouble with", "streammax"),
    ("the dispute I opened for my subscription", "streammax"),
    ("why did my dispute get turned down", "rejection"),
    ("my trip to Portugal", "lisbon"),
    ("when I asked you to text me instead", "sms"),
    ("the reminder about my next trip", "porto-reminder"),
    ("what I pay for foreign purchases", "fx"),
    ("my broken card", "replacement"),
    ("the little charge from the pastry shop", "bakery"),
    ("the coffee purchase", "coffee"),
    ("asking for more credit", "limit"),
    ("the case number for StreamMax", "streammax"),
]


def keyword_ranker(texts: list[str]):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE VIRTUAL TABLE docs USING fts5(body, tokenize='unicode61')")
    conn.executemany("INSERT INTO docs(rowid, body) VALUES (?, ?)", [(i, t) for i, t in enumerate(texts)])

    def rank(query: str, limit: int) -> list[int]:
        tokens = [t.lower() for t in re.findall(r"\w+", query)]
        match = " OR ".join(f'"{t}"' for t in tokens)
        rows = conn.execute("SELECT rowid FROM docs WHERE docs MATCH ? ORDER BY bm25(docs) LIMIT ?", (match, limit)).fetchall()
        return [row[0] for row in rows]

    return rank


def embedding_ranker(texts: list[str]):
    vectors = embed_texts(texts)
    return lambda query, limit: [index for index, _ in top_matches(query, vectors, limit)]


def recall_at(ranker, labels: list[str], queries: list[tuple[str, str]], k: int) -> tuple[float, list[str]]:
    misses = [q for q, expected in queries if labels.index(expected) not in ranker(q, k)]
    return 1 - len(misses) / len(queries), misses


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    centre = (successes + z * z / 2) / (n + z * z)
    half = z * math.sqrt(successes * (n - successes) / n + z * z / 4) / (n + z * z)
    return max(0.0, centre - half), min(1.0, centre + half)


def score_cell(score: float, n: int) -> str:
    low, high = wilson(round(score * n), n)
    return f"{score:.2f} [{low:.2f}, {high:.2f}]"


def main() -> None:
    policy = sorted(POLICY_DIR.glob("*.md"))
    policy_labels, policy_texts = [p.stem for p in policy], [p.read_text() for p in policy]
    episode_labels, episode_texts = [e[0] for e in EPISODES], [e[1] for e in EPISODES]
    lines = ["# Retrieval evaluation", "", "Generated by `python eval_retrieval.py`. No model calls; keyword = SQLite FTS5/BM25 with "
             "OR-joined tokens (ADK's built-in `SqliteMemoryService` method), embeddings = fastembed `BAAI/bge-small-en-v1.5`.", ""]
    distractor_labels = episode_labels + [d[0] for d in DISTRACTORS]
    distractor_texts = episode_texts + [d[1] for d in DISTRACTORS]
    for name, labels, texts, queries, k_values in (
        ("Policy KB (6 documents)", policy_labels, policy_texts, POLICY_QUERIES, (1, 2)),
        ("Episode history (10 episodes, one customer)", episode_labels, episode_texts, EPISODE_QUERIES, (1, 3)),
        ("Distractor test: the same history plus 8 near-miss episodes", distractor_labels, distractor_texts, EPISODE_QUERIES, (1, 3)),
    ):
        lines += [f"## {name}: {len(queries)} labelled queries", "", "recall [Wilson 95% interval]", "",
                  "| method | " + " | ".join(f"recall@{k}" for k in k_values) + " | missed at recall@1 |", "|---|---|---|---|"]
        for method, make in (("keyword (FTS5/BM25)", keyword_ranker), ("embeddings", embedding_ranker)):
            ranker = make(texts)
            scores = [recall_at(ranker, labels, queries, k) for k in k_values]
            missed = "; ".join(scores[0][1]) or "none"
            lines.append(f"| {method} | " + " | ".join(score_cell(s[0], len(queries)) for s in scores) + f" | {missed} |")
        lines.append("")
    lines += ["The intervals are wide: these sets show embeddings beating keyword search on paraphrase, not a precise recall.", ""]
    vectors = embed_texts(policy_texts)
    answerable = [top_matches(q, vectors, 1)[0][1] for q, _ in POLICY_QUERIES]
    unanswerable = [top_matches(q, vectors, 1)[0][1] for q in UNANSWERABLE_QUERIES]
    lines += ["## Questions the KB cannot answer", "",
              f"Best embedding score for answerable queries: min {min(answerable):.3f}, mean {mean(answerable):.3f}. "
              f"For unanswerable ones ({', '.join(UNANSWERABLE_QUERIES)}): max {max(unanswerable):.3f}, mean {mean(unanswerable):.3f}.", "",
              "If the two ranges overlap, no similarity threshold can tell 'not in the KB' apart from 'answerable', so the "
              "procedure's rule 2 (quote no Kestrel figure that was not retrieved) has to carry that load rather than the retriever.", ""]
    out = CODE_DIR / "evidence" / "retrieval" / "results.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
