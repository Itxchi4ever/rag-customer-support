import json

import faiss
import numpy as np

from embeddings.embedding_model import EmbeddingModel


INDEX_FILE = "vectorstore/faiss.index"
METADATA_FILE = "vectorstore/metadata.json"


class VectorSearch:
    def __init__(self):
        self.index = faiss.read_index(INDEX_FILE)

        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            self.metadata = json.load(file)

        self.embedding_model = EmbeddingModel()

    def search(self, query, top_k=5, product=None):
        """
        Search the vector database for relevant chunks.

        Optionally filter results by product.
        """

        query_embedding = self.embedding_model.embed_query(query)

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        # Search more results when filtering
        search_k = self.index.ntotal if product else top_k

        scores, indices = self.index.search(
            query_embedding,
            search_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            result = self.metadata[index].copy()

            if product:
                result_product = result["metadata"].get("product")

                if result_product != product:
                    continue

            result["score"] = float(score)
            results.append(result)

            if len(results) >= top_k:
                break

        return results