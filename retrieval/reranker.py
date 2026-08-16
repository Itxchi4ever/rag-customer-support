from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:
    def __init__(self):
        self.model = CrossEncoder(MODEL_NAME)

    def rerank(self, query, documents, top_k=5):
        """
        Rerank retrieved documents based on
        query-document relevance.
        """

        if not documents:
            return []

        pairs = [
            (query, document["text"])
            for document in documents
        ]

        scores = self.model.predict(pairs)

        reranked_documents = []

        for document, score in zip(documents, scores):
            result = document.copy()
            result["rerank_score"] = float(score)

            reranked_documents.append(result)

        reranked_documents.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked_documents[:top_k]