"""Local embeddings and the policy knowledge base (external / retrieval memory).

Why a local embedding model (fastembed + BAAI/bge-small-en-v1.5, 384 dimensions, ONNX on CPU):
  - DeepSeek offers no embeddings endpoint, and sending customer episode text to a
    second vendor just to index it is a data-processing decision a demo cannot justify.
  - Recall has to survive paraphrase ("that streaming thing" -> "StreamMax"), which keyword
    search does not; ADK's built-in SqliteMemoryService is keyword (FTS5) only.
  - It is about 64 MB, needs no GPU or torch, and is downloaded once into var/.
Transactions and cases are never searched this way: those are exact lookups (see world.py).
"""

import functools
import os
from pathlib import Path

import numpy as np

CODE_DIR = Path(__file__).resolve().parent.parent
POLICY_DIR = Path(__file__).resolve().parent / "policy_kb"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMS = 384


@functools.cache
def _embedder():
    from fastembed import TextEmbedding

    cache_dir = os.environ.get("CARDCARE_EMBED_CACHE", str(CODE_DIR / "var" / "embedding-model"))
    return TextEmbedding(EMBEDDING_MODEL, cache_dir=cache_dir)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Unit-length embeddings, so a dot product is cosine similarity."""
    return [vector.tolist() for vector in _embedder().embed(list(texts))]


def top_matches(query: str, vectors: list[list[float]], limit: int) -> list[tuple[int, float]]:
    """(index into `vectors`, cosine score) pairs, best first."""
    if not vectors:
        return []
    scores = np.array(vectors) @ np.array(embed_texts([query])[0])
    return [(int(index), round(float(scores[index]), 3)) for index in np.argsort(-scores)[:limit]]


@functools.cache
def _policy_index() -> tuple[tuple[tuple[str, str], ...], tuple[tuple[float, ...], ...]]:
    documents = tuple((path.stem, path.read_text()) for path in sorted(POLICY_DIR.glob("*.md")))
    vectors = tuple(tuple(vector) for vector in embed_texts([text for _, text in documents]))
    return documents, vectors


def search_policy(query: str, limit: int = 2) -> list[dict]:
    """Top Kestrel policy documents for a question. App-scoped: identical for every customer."""
    documents, vectors = _policy_index()
    return [
        {"document": documents[index][0], "score": score, "text": documents[index][1]}
        for index, score in top_matches(query, [list(v) for v in vectors], limit)
    ]
