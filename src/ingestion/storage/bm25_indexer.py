"""BM25 inverted index builder and persistence layer."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

from core.types import ChunkRecord


class BM25Indexer:
    """Build and persist BM25-style inverted index from sparse chunk vectors."""

    def __init__(
        self,
        settings: Any,
        *,
        index_dir: str | None = None,
    ) -> None:
        self.settings = settings
        self.index_dir = Path(index_dir or self._resolve_index_dir(settings))
        self.index_file = self.index_dir / "index.json"

        self._doc_vectors: dict[str, dict[str, float]] = {}
        self._doc_sources: dict[str, str] = {}
        self.idf: dict[str, float] = {}
        self.inverted_index: dict[str, list[dict[str, float | str]]] = {}
        self.doc_count = 0

    def upsert(self, records: list[ChunkRecord], trace: Any | None = None) -> int:
        """Upsert sparse records into in-memory index and persist to disk."""
        self._validate_records(records)
        for record in records:
            sparse = dict(record.sparse_vector or {})
            self._doc_vectors[record.id] = sparse
            source = str(record.metadata.get("source_path", "")).strip()
            self._doc_sources[record.id] = source

        self._rebuild_index()
        self.persist()

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "storage_bm25_upsert",
                upsert_count=len(records),
                doc_count=self.doc_count,
                vocab_size=len(self.idf),
            )
        return len(records)

    def remove_document(self, source: str, trace: Any | None = None) -> int:
        """Remove all chunk records belonging to the given source path."""
        if not isinstance(source, str) or not source.strip():
            raise ValueError("source must be a non-empty string")
        source_norm = source.strip()

        to_remove = [doc_id for doc_id, src in self._doc_sources.items() if src == source_norm]
        for doc_id in to_remove:
            self._doc_sources.pop(doc_id, None)
            self._doc_vectors.pop(doc_id, None)

        if to_remove:
            self._rebuild_index()
            self.persist()

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "storage_bm25_remove_document",
                source=source_norm,
                removed_count=len(to_remove),
                doc_count=self.doc_count,
            )
        return len(to_remove)

    def query(self, keywords: list[str], top_k: int = 5) -> list[dict[str, Any]]:
        """Query BM25 index by keyword list and return ranked chunk ids."""
        if not isinstance(keywords, list):
            raise TypeError("keywords must be a list")
        if isinstance(top_k, bool) or not isinstance(top_k, int):
            raise TypeError("top_k must be an integer")
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        tokens = self._normalize_keywords(keywords)
        if not tokens:
            return []
        if not self.inverted_index:
            return []

        query_tf = Counter(tokens)
        scores: dict[str, float] = {}
        for term, qtf in query_tf.items():
            postings = self.inverted_index.get(term, [])
            if not postings:
                continue
            for item in postings:
                chunk_id = str(item["chunk_id"])
                doc_weight = float(item["weight"])
                scores[chunk_id] = scores.get(chunk_id, 0.0) + (float(qtf) * doc_weight)

        ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))[:top_k]
        return [{"chunk_id": chunk_id, "score": score} for chunk_id, score in ranked]

    def persist(self) -> None:
        """Persist current index state to disk."""
        self.index_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": 1,
            "doc_count": self.doc_count,
            "doc_vectors": self._doc_vectors,
            "doc_sources": self._doc_sources,
            "idf": self.idf,
            "inverted_index": self.inverted_index,
        }
        self.index_file.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")

    def load(self) -> None:
        """Load index state from disk if available."""
        if not self.index_file.exists():
            self._doc_vectors = {}
            self._doc_sources = {}
            self.idf = {}
            self.inverted_index = {}
            self.doc_count = 0
            return

        payload = json.loads(self.index_file.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("bm25 index file must contain a JSON object")

        doc_vectors = payload.get("doc_vectors", {})
        doc_sources = payload.get("doc_sources", {})
        if not isinstance(doc_vectors, dict) or not isinstance(doc_sources, dict):
            raise ValueError("bm25 index file missing required mappings")

        normalized_vectors: dict[str, dict[str, float]] = {}
        for doc_id, vector in doc_vectors.items():
            if not isinstance(doc_id, str):
                continue
            if not isinstance(vector, dict):
                continue
            norm_vec: dict[str, float] = {}
            for term, value in vector.items():
                if not isinstance(term, str):
                    continue
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    continue
                numeric = float(value)
                if math.isfinite(numeric) and numeric > 0:
                    norm_vec[term] = numeric
            normalized_vectors[doc_id] = norm_vec

        normalized_sources: dict[str, str] = {}
        for doc_id, src in doc_sources.items():
            if isinstance(doc_id, str) and isinstance(src, str):
                normalized_sources[doc_id] = src

        self._doc_vectors = normalized_vectors
        self._doc_sources = normalized_sources
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        doc_count = len(self._doc_vectors)
        self.doc_count = doc_count
        if doc_count == 0:
            self.idf = {}
            self.inverted_index = {}
            return

        doc_freq: Counter[str] = Counter()
        for vector in self._doc_vectors.values():
            doc_freq.update(set(vector.keys()))

        idf: dict[str, float] = {}
        for term, df in doc_freq.items():
            idf[term] = math.log(1.0 + ((doc_count - df + 0.5) / (df + 0.5)))

        inverted: dict[str, list[dict[str, float | str]]] = {}
        for chunk_id, vector in self._doc_vectors.items():
            for term, weight in vector.items():
                bm25_weight = float(weight) * idf.get(term, 0.0)
                if bm25_weight <= 0:
                    continue
                inverted.setdefault(term, []).append(
                    {"chunk_id": chunk_id, "weight": bm25_weight}
                )

        for term, postings in inverted.items():
            postings.sort(key=lambda item: (-float(item["weight"]), str(item["chunk_id"])))
            inverted[term] = postings

        self.idf = idf
        self.inverted_index = inverted

    @staticmethod
    def _normalize_keywords(keywords: list[str]) -> list[str]:
        tokens: list[str] = []
        for item in keywords:
            if not isinstance(item, str):
                continue
            text = item.strip().lower()
            if not text:
                continue
            tokens.extend(token for token in text.split() if token)
        return tokens

    @staticmethod
    def _validate_records(records: list[ChunkRecord]) -> None:
        if not isinstance(records, list):
            raise TypeError("records must be a list")
        for index, record in enumerate(records):
            if not isinstance(record, ChunkRecord):
                raise TypeError(f"record at index {index} must be a ChunkRecord")

    @staticmethod
    def _resolve_index_dir(settings: Any) -> str:
        if isinstance(settings, dict):
            ingestion = settings.get("ingestion")
        else:
            ingestion = getattr(settings, "ingestion", None)
        if isinstance(ingestion, dict):
            section = ingestion.get("bm25_indexer")
            if isinstance(section, dict):
                value = section.get("index_dir")
                if isinstance(value, str) and value.strip():
                    return value.strip()
        return "data/db/bm25"
