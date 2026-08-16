import json
from pathlib import Path

from document_loader import load_documents
from cleaner import clean_text
from chunker import chunk_text
from metadata import create_metadata


def process_documents(
    input_path="data/raw",
    output_path="data/chunks"
):
    
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    documents = load_documents(input_path)

    all_chunks = []

    for document in documents:
        filename = document["filename"]

        # Step 1: Clean document
        cleaned_text = clean_text(document["text"])

        # Step 2: Create chunks
        chunks = chunk_text(cleaned_text)

        # Step 3: Add metadata to each chunk
        for chunk_id, chunk in enumerate(chunks):
            metadata = create_metadata(
                filename,
                chunk_id
            )

            all_chunks.append({
                "text": chunk,
                "metadata": metadata
            })

    # Save all processed chunks
    output_file = output_path / "chunks.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"Processed {len(documents)} documents.")
    print(f"Created {len(all_chunks)} chunks.")
    print(f"Saved chunks to: {output_file}")


if __name__ == "__main__":
    process_documents()