from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_documents(self, texts):
        """
        Convert multiple text chunks into embeddings.
        """
        return self.model.encode(
            texts,
            normalize_embeddings=True
        )

    def embed_query(self, query):
        """
        Convert a user query into an embedding.
        """
        return self.model.encode(
            query,
            normalize_embeddings=True
        )