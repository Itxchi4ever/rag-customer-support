import json
from pathlib import Path

import faiss
import numpy as np

from embeddings.embedding_model import EmbeddingModel


CHUNKS_FILE = "data/chunks/chunks.json"
INDEX_FILE = "vectorstore/faiss.index"
METADATA_FILE = "vectorstore/metadata.json"


def create_index():
    # Load chunks
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No chunks found in chunks.json")

    # Extract text
    texts = [chunk["text"] for chunk in chunks]

    # Create embeddings
    embedding_model = EmbeddingModel()
    embeddings = embedding_model.embed_documents(texts)

    # Convert embeddings to NumPy float32
    embeddings = np.asarray(embeddings, dtype="float32")

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, INDEX_FILE)

    # Save corresponding metadata
    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=2, ensure_ascii=False)

    print(f"Loaded chunks: {len(chunks)}")
    print(f"Embedding dimension: {dimension}")
    print(f"FAISS vectors stored: {index.ntotal}")
    print(f"Index saved to: {INDEX_FILE}")
    print(f"Metadata saved to: {METADATA_FILE}")


if __name__ == "__main__":
    create_index()