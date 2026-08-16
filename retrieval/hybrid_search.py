import json
from pathlib import Path

from rank_bm25 import BM25Okapi

from vectorstore.search import VectorSearch


CHUNKS_FILE = Path("data/chunks/chunks.json")


class HybridSearch:
    def __init__(self):
        self.vector_search = VectorSearch()

        with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
            self.chunks = json.load(file)

        self.tokenized_chunks = [
            chunk["text"].lower().split()
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(self.tokenized_chunks)

    def _get_chunk_key(self, chunk):
        """
        Create a unique identifier for a chunk.

        chunk_id may repeat across different documents,
        so source + chunk_id is used instead.
        """

        metadata = chunk["metadata"]

        return (
            f"{metadata['source']}:"
            f"{metadata['chunk_id']}"
        )

    def semantic_search(self, query, top_k=5, product=None):
        """
        Perform semantic search using FAISS.
        """

        return self.vector_search.search(
            query,
            top_k=top_k,
            product=product
        )

    def keyword_search(self, query, top_k=5, product=None):
        """
        Perform keyword search using BM25.
        """

        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = scores.argsort()[::-1]

        results = []

        for index in ranked_indices:
            chunk = self.chunks[index]

            if product:
                chunk_product = (
                    chunk["metadata"].get("product")
                )

                if chunk_product != product:
                    continue

            result = chunk.copy()
            result["score"] = float(scores[index])

            results.append(result)

            if len(results) >= top_k:
                break

        return results

    def search(self, query, top_k=5, product=None):
        """
        Perform semantic and keyword search,
        then combine the rankings using RRF.
        """

        semantic_results = self.semantic_search(
            query,
            top_k=top_k,
            product=product
        )

        keyword_results = self.keyword_search(
            query,
            top_k=top_k,
            product=product
        )

        rrf_scores = {}

        # Semantic search contribution
        for rank, result in enumerate(
            semantic_results,
            start=1
        ):
            chunk_key = self._get_chunk_key(result)

            rrf_scores[chunk_key] = (
                rrf_scores.get(chunk_key, 0)
                + 1 / (60 + rank)
            )

        # Keyword search contribution
        for rank, result in enumerate(
            keyword_results,
            start=1
        ):
            chunk_key = self._get_chunk_key(result)

            rrf_scores[chunk_key] = (
                rrf_scores.get(chunk_key, 0)
                + 1 / (60 + rank)
            )

        ranked_chunks = sorted(
            rrf_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        # Create lookup using globally unique keys
        chunk_lookup = {
            self._get_chunk_key(chunk): chunk
            for chunk in self.chunks
        }

        results = []

        for chunk_key, score in ranked_chunks[:top_k]:
            result = chunk_lookup[chunk_key].copy()

            result["score"] = score

            results.append(result)

        return results