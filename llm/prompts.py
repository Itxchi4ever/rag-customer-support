SYSTEM_PROMPT = """
You are a customer support assistant.

Answer the user's question using only the provided context
and relevant conversation history.

Rules:
1. Do not make up information.
2. If the answer cannot be found in the provided context,
   say that you do not have enough information.
3. Keep the answer clear and helpful.
4. Give step-by-step instructions when appropriate.
5. Use the product information in the context carefully.
6. Use conversation history to understand references such as
   "it", "that", "this", or "the previous step".
"""


def build_prompt(query, retrieved_chunks, conversation_history=None):
    """
    Build the prompt using retrieved context and conversation history.
    """

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Context {i}]\n{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    history = ""

    if conversation_history:
        history_parts = []

        for message in conversation_history:
            history_parts.append(
                f"{message['role'].capitalize()}: {message['content']}"
            )

        history = "\n".join(history_parts)

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{history}

Knowledge Base Context:
{context}

Current User Question:
{query}

Answer:
"""

    return prompt