from pathlib import Path


def create_metadata(filename, chunk_id):
    

    stem = Path(filename).stem.lower()

    metadata = {
        "source": filename,
        "chunk_id": chunk_id,
    }

    # Product identification
    if "smartwatch" in stem:
        metadata["product"] = "smartwatch"
    elif "techbook" in stem:
        metadata["product"] = "techbook"
    elif "techbuds" in stem:
        metadata["product"] = "techbuds"
    else:
        metadata["product"] = "general"

    # Document type
    if "troubleshooting" in stem:
        metadata["document_type"] = "troubleshooting"
    elif "manual" in stem:
        metadata["document_type"] = "manual"
    elif "faq" in stem:
        metadata["document_type"] = "faq"
    elif "policy" in stem:
        policy_name = stem.replace("_policy", "")
        metadata["document_type"] = "policy"
        metadata["policy_type"] = policy_name
    else:
        metadata["document_type"] = "general"

    return metadata