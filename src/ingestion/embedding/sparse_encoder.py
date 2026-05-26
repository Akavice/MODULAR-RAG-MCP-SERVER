"""Sparse BM25-style encoder for ingestion chunks."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from core.types import Chunk, ChunkRecord


_DEFAULT_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}
_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")


class SparseEncoder:
    """Compute BM25-style sparse term weights for chunks."""

    def __init__(self, settings: Any) -> None:
        self.settings = settings
        section = self._extract_sparse_settings(settings)
        self.k1 = self._to_positive_float(section.get("k1", 1.5), field_name="k1")
        self.b = self._to_b_float(section.get("b", 0.75))
        self.min_token_length = self._to_positive_int(
            section.get("min_token_length", 2),
            field_name="min_token_length",
        )
        self.remove_stopwords = self._to_bool(section.get("remove_stopwords", True))

    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        self._validate_chunks(chunks)
        if not chunks:
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage(
                    "embed_sparse_encoder",
                    chunk_count=0,
                    vocab_size=0,
                    avg_doc_len=0.0,
                    k1=self.k1,
                    b=self.b,
                )
            return []

        tokenized_docs = [self._tokenize(chunk.text) for chunk in chunks]
        doc_lens = [len(tokens) for tokens in tokenized_docs]
        avg_doc_len = sum(doc_lens) / len(doc_lens) if doc_lens else 0.0

        doc_freq: Counter[str] = Counter()
        for tokens in tokenized_docs:
            if not tokens:
                continue
            doc_freq.update(set(tokens))

        chunk_records: list[ChunkRecord] = []
        doc_count = len(chunks)
        for chunk, tokens, doc_len in zip(chunks, tokenized_docs, doc_lens):
            tf = Counter(tokens)
            sparse_vector: dict[str, float] = {}

            for term, freq in tf.items():
                df = doc_freq.get(term, 0)
                if df <= 0:
                    continue
                idf = math.log(1.0 + ((doc_count - df + 0.5) / (df + 0.5)))
                denom_norm = self.k1 * (1.0 - self.b + self.b * (doc_len / max(avg_doc_len, 1e-9)))
                weight = idf * ((freq * (self.k1 + 1.0)) / (freq + denom_norm))
                if math.isfinite(weight) and weight > 0:
                    sparse_vector[term] = float(weight)

            record = ChunkRecord(
                id=chunk.id,
                text=chunk.text,
                metadata=dict(chunk.metadata),
                dense_vector=None,
                sparse_vector=sparse_vector,
            )
            chunk_records.append(record)

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "embed_sparse_encoder",
                chunk_count=len(chunks),
                vocab_size=len(doc_freq),
                avg_doc_len=avg_doc_len,
                k1=self.k1,
                b=self.b,
            )

        return chunk_records

    def _tokenize(self, text: str) -> list[str]:
        if not isinstance(text, str):
            return []
        tokens = [token.lower() for token in _TOKEN_PATTERN.findall(text)]
        if self.min_token_length > 1:
            tokens = [token for token in tokens if len(token) >= self.min_token_length]
        if self.remove_stopwords:
            tokens = [token for token in tokens if token not in _DEFAULT_STOP_WORDS]
        return tokens

    @staticmethod
    def _validate_chunks(chunks: list[Chunk]) -> None:
        if not isinstance(chunks, list):
            raise TypeError("chunks must be a list")
        for index, chunk in enumerate(chunks):
            if not isinstance(chunk, Chunk):
                raise TypeError(f"chunk at index {index} must be a Chunk")

    @staticmethod
    def _extract_sparse_settings(settings: Any) -> dict[str, Any]:
        if isinstance(settings, dict):
            ingestion = settings.get("ingestion")
        else:
            ingestion = getattr(settings, "ingestion", None)

        if isinstance(ingestion, dict):
            dense_section = ingestion.get("sparse_encoder")
            if isinstance(dense_section, dict):
                return dict(dense_section)
        return {}

    @staticmethod
    def _to_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return bool(value)

    @staticmethod
    def _to_positive_int(value: Any, *, field_name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{field_name} must be an integer")
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")
        return value

    @staticmethod
    def _to_positive_float(value: Any, *, field_name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be numeric")
        numeric = float(value)
        if not math.isfinite(numeric) or numeric <= 0:
            raise ValueError(f"{field_name} must be a finite number > 0")
        return numeric

    @staticmethod
    def _to_b_float(value: Any) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("b must be numeric")
        numeric = float(value)
        if not math.isfinite(numeric) or numeric < 0 or numeric > 1:
            raise ValueError("b must be a finite number in [0, 1]")
        return numeric
