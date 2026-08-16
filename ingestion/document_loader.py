from pathlib import Path

def load_documents(data_path="data/raw"):

    document = []

    data_path=Path(data_path)

    for file_path in data_path.rglob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

            document.append({
                "filename": file_path.name,
                "filepath": str(file_path),
                "text": text
            })

    return document