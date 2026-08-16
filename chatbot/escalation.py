import json
from datetime import datetime
from pathlib import Path


ESCALATION_KEYWORDS = [
    "human",
    "agent",
    "representative",
    "customer support",
    "talk to someone",
    "speak to someone",
    "complaint",
    "refund",
    "legal",
]

TICKETS_FILE = Path("data/tickets/tickets.json")


def should_escalate(message):
    """
    Determine whether a user message should be escalated
    to human customer support.
    """

    message = message.lower()

    return any(
        keyword in message
        for keyword in ESCALATION_KEYWORDS
    )


def create_support_ticket(
    user_message,
    conversation_history,
    product=None
):
    """
    Create and persist a structured support ticket.
    """

    ticket = {
        "ticket_id": f"TICKET-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "product": product or "unknown",
        "issue": user_message,
        "conversation": conversation_history,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }

    save_ticket(ticket)

    return ticket


def save_ticket(ticket):
    """
    Save a support ticket to the local ticket database.
    """

    TICKETS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if TICKETS_FILE.exists():
        with open(TICKETS_FILE, "r", encoding="utf-8") as file:
            tickets = json.load(file)
    else:
        tickets = []

    tickets.append(ticket)

    with open(TICKETS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            tickets,
            file,
            indent=2,
            ensure_ascii=False
        )


def get_all_tickets():
    """
    Retrieve all persisted support tickets.
    """

    if not TICKETS_FILE.exists():
        return []

    with open(TICKETS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def escalation_response():
    """
    Return the response shown when escalation is required.
    """

    return (
        "I understand. This issue may require assistance from "
        "our customer support team. I've created a support ticket "
        "for human follow-up."
    )