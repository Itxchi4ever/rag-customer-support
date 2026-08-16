from chatbot.memory import ConversationMemory
from chatbot.escalation import (
    should_escalate,
    escalation_response,
    create_support_ticket
)
from chatbot.safety import (
    detect_prompt_injection,
    safety_response
)
from llm.rag import RAGPipeline


def detect_product(message):
    """
    Detect the product mentioned in the user's message.
    """

    message = message.lower()

    products = {
        "smartwatch": ["smartwatch", "watch"],
        "techbook": ["techbook", "laptop", "notebook"],
        "techbuds": ["techbuds", "earbuds", "earphones"]
    }

    for product, keywords in products.items():
        for keyword in keywords:
            if keyword in message:
                return product

    return None


class Conversation:
    def __init__(self, top_k=5):
        self.memory = ConversationMemory()
        self.rag = RAGPipeline(top_k=top_k)
        self.last_ticket = None

    def chat(self, user_message):
        """
        Process a user message while maintaining conversation
        history, product context, escalation, and safety handling.
        """

        self.memory.add_message("user", user_message)

        if detect_prompt_injection(user_message):
            answer = safety_response()

        else:
            product = detect_product(user_message)

            if product:
                self.memory.set_product(product)
            else:
                product = self.memory.get_product()

            if should_escalate(user_message):
                self.last_ticket = create_support_ticket(
                    user_message=user_message,
                    conversation_history=self.memory.get_history(),
                    product=product
                )

                answer = escalation_response()

            else:
                answer = self.rag.answer(
                    user_message,
                    conversation_history=self.memory.get_history(),
                    product=product
                )

        self.memory.add_message("assistant", answer)

        return answer

    def get_history(self):
        return self.memory.get_history()

    def get_last_ticket(self):
        return self.last_ticket

    def clear_history(self):
        self.memory.clear()
        self.last_ticket = None