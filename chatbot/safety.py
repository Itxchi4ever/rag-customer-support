INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "ignore the instructions",
    "disregard previous instructions",
    "disregard all previous instructions",
    "forget your instructions",
    "override your instructions",
    "system prompt",
    "reveal your prompt",
    "show me your prompt",
]


def detect_prompt_injection(message):
    """
    Detect common prompt-injection attempts.

    This is a basic defensive layer, not a complete
    security solution.
    """

    message = message.lower().strip()

    for pattern in INJECTION_PATTERNS:
        if pattern in message:
            return True

    return False


def safety_response():
    """
    Response returned when a suspicious instruction
    is detected.
    """

    return (
        "I can help with questions about our products and "
        "customer support information, but I can't follow "
        "instructions that attempt to override my operating rules."
    )