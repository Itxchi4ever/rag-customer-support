from retrieval.retriever import Retriever
from llm.prompts import build_prompt
from llm.generator import HuggingFaceGenerator


class RAGPipeline:
    def __init__(self, top_k=5):
        self.retriever = Retriever(top_k=top_k)
        self.generator = HuggingFaceGenerator()

    def answer(self, query, conversation_history=None, product=None):
        """
        Retrieve relevant context and generate a grounded answer.
        """

        retrieved_chunks = self.retriever.retrieve(
            query,
            product=product
            )

        if not retrieved_chunks:
            return "I could not find relevant information in the knowledge base."

        prompt = build_prompt(
            query,
            retrieved_chunks,
            conversation_history
        )

        answer = self.generator.generate(prompt)

        return answer