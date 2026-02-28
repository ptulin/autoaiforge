"""
ChromaDB vector store — rebuilt each run from SQLite to avoid large binary commits.
Uses sentence-transformers (local, free) for embeddings.
"""

import re
from typing import Optional

from utils.logger import get_logger
import config

log = get_logger("vector_store")

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    CHROMA_OK = True
except ImportError:
    CHROMA_OK = False
    log.warning("chromadb not installed — vector search disabled")

try:
    from sentence_transformers import SentenceTransformer
    ST_OK = True
except ImportError:
    ST_OK = False
    log.warning("sentence-transformers not installed — using fallback keyword search")


class VectorStore:
    """
    In-memory ChromaDB collection for the current run.
    We do NOT persist to disk to keep repo size small.
    Embeddings are recomputed fresh each run.
    """

    COLLECTION_NAME = "news_embeddings"

    def __init__(self):
        self._client = None
        self._collection = None
        self._model: Optional["SentenceTransformer"] = None
        self._ready = False

        if CHROMA_OK and ST_OK:
            self._init()
        else:
            log.warning("VectorStore running in fallback mode (no embeddings)")

    def _init(self):
        try:
            self._client = chromadb.EphemeralClient()
            self._collection = self._client.create_collection(
                name=self.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
            log.info("Loading sentence-transformer model …")
            self._model = SentenceTransformer(config.EMBED_MODEL)
            self._ready = True
            log.info("VectorStore ready")
        except Exception as e:
            log.error(f"VectorStore init failed: {e}")
            self._ready = False

    # ── Ingestion ─────────────────────────────────────────────────────────────

    def index_items(self, items: list[tuple[str, str]]) -> int:
        """
        Index list of (id, text) tuples.
        Returns number indexed.
        """
        if not self._ready or not items:
            return 0

        ids   = [i[0] for i in items]
        texts = [i[1] for i in items]

        # Batch embed (ChromaDB handles size limits internally)
        BATCH = 256
        total = 0
        for start in range(0, len(ids), BATCH):
            batch_ids   = ids[start : start + BATCH]
            batch_texts = texts[start : start + BATCH]
            try:
                embeddings = self._model.encode(
                    batch_texts, show_progress_bar=False
                ).tolist()
                # Deduplicate ids (ChromaDB will error on duplicate adds)
                existing = set(self._collection.get(ids=batch_ids)["ids"])
                new_ids   = [i for i in batch_ids if i not in existing]
                new_texts = [t for i, t in zip(batch_ids, batch_texts) if i not in existing]
                new_embs  = [e for i, e in zip(batch_ids, embeddings) if i not in existing]
                if new_ids:
                    self._collection.add(
                        ids=new_ids,
                        documents=new_texts,
                        embeddings=new_embs,
                    )
                    total += len(new_ids)
            except Exception as e:
                log.warning(f"Batch index error: {e}")
        log.info(f"Indexed {total} items into vector store")
        return total

    # ── Query ─────────────────────────────────────────────────────────────────

    def query(self, query_text: str, n_results: int = 20) -> list[dict]:
        """
        Return top-n semantically similar documents.
        Falls back to empty list if not ready.
        """
        if not self._ready:
            return []
        try:
            embedding = self._model.encode([query_text]).tolist()
            results   = self._collection.query(
                query_embeddings=embedding,
                n_results=min(n_results, self._collection.count() or 1),
                include=["documents", "distances"],
            )
            docs = results.get("documents", [[]])[0]
            dists = results.get("distances", [[]])[0]
            return [
                {"text": doc, "distance": dist}
                for doc, dist in zip(docs, dists)
            ]
        except Exception as e:
            log.error(f"Vector query failed: {e}")
            return []

    def get_all_texts(self) -> list[str]:
        """Return all indexed documents."""
        if not self._ready:
            return []
        try:
            result = self._collection.get(include=["documents"])
            return result.get("documents", [])
        except Exception as e:
            log.error(f"get_all_texts failed: {e}")
            return []

    def count(self) -> int:
        if not self._ready:
            return 0
        try:
            return self._collection.count()
        except Exception:
            return 0
