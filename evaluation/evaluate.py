import json

from retrieval.retriever import Retriever


QUESTIONS_FILE = "evaluation/test_questions.json"


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_product(product):
    """
    Normalize product names for comparison.
    """

    if not product:
        return None

    return product.lower().strip()


def evaluate_retrieval():
    questions = load_questions()

    retriever = Retriever(
        top_k=5,
        candidate_k=15
    )

    total_questions = len(questions)
    correct_questions = 0

    print("\n=== RAG Retrieval Evaluation ===\n")

    for i, item in enumerate(questions, start=1):
        question = item["question"]

        expected_product = normalize_product(
            item["expected_product"]
        )

        results = retriever.retrieve(
            question,
            product=expected_product
        )

        retrieved_products = []

        for result in results:
            product = result["metadata"].get("product")

            if product:
                retrieved_products.append(
                    normalize_product(product)
                )

        if expected_product is None:
            correct = len(results) > 0
        else:
            correct = expected_product in retrieved_products

        if correct:
            correct_questions += 1

        print(f"Question {i}: {question}")
        print(f"Expected product: {expected_product}")
        print(f"Retrieved products: {retrieved_products}")
        print(f"Result: {'PASS' if correct else 'FAIL'}")
        print("-" * 60)

    accuracy = (
        correct_questions / total_questions
        if total_questions
        else 0
    )

    print("\n=== Evaluation Summary ===")
    print(f"Total questions: {total_questions}")
    print(f"Correct: {correct_questions}")
    print(f"Incorrect: {total_questions - correct_questions}")
    print(f"Retrieval accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    evaluate_retrieval()