from retrieval.hybrid_search import HybridSearch
from retrieval.reranker import Reranker


class Retriever:
    def __init__(
        self,
        top_k=5,
        candidate_k=15,
        score_threshold=None
    ):
        self.hybrid_search = HybridSearch()
        self.reranker = Reranker()

        self.top_k = top_k
        self.candidate_k = candidate_k
        self.score_threshold = score_threshold

    def _remove_duplicate_chunks(self, documents):
        """
        Remove duplicate chunks based on their text.
        """

        seen = set()
        unique_documents = []

        for document in documents:
            text = document["text"].strip()

            if text in seen:
                continue

            seen.add(text)
            unique_documents.append(document)

        return unique_documents

    def _limit_context(self, documents, max_characters=12000):
        """
        Limit the total amount of context returned to the LLM.
        """

        selected_documents = []
        total_characters = 0

        for document in documents:
            text_length = len(document["text"])

            if total_characters + text_length > max_characters:
                break

            selected_documents.append(document)
            total_characters += text_length

        return selected_documents

    def retrieve(self, query, product=None):
        """
        Retrieve relevant chunks using hybrid search,
        reranking, deduplication, and context optimization.
        """

        candidates = self.hybrid_search.search(
            query,
            top_k=self.candidate_k,
            product=product
        )

        if not candidates:
            return []

        reranked_results = self.reranker.rerank(
            query,
            candidates,
            top_k=self.top_k
        )

        # Remove duplicate information
        unique_results = self._remove_duplicate_chunks(
            reranked_results
        )

        retrieved_chunks = []

        for result in unique_results:

            if (
                self.score_threshold is not None
                and result["rerank_score"] < self.score_threshold
            ):
                continue

            retrieved_chunks.append({
                "text": result["text"],
                "score": result["score"],
                "rerank_score": result["rerank_score"],
                "metadata": result["metadata"]
            })

        # Limit total context sent toward the LLM
        retrieved_chunks = self._limit_context(
            retrieved_chunks
        )

        return retrieved_chunks