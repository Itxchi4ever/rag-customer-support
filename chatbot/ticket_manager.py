import json
from pathlib import Path


TICKETS_FILE = Path("data/tickets/tickets.json")

VALID_STATUSES = {
    "open",
    "in_progress",
    "resolved"
}


class TicketManager:
    def __init__(self):
        TICKETS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def get_all_tickets(self):
        """
        Return all support tickets.
        """

        if not TICKETS_FILE.exists():
            return []

        with open(TICKETS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_ticket(self, ticket_id):
        """
        Find a ticket using its ticket ID.
        """

        tickets = self.get_all_tickets()

        for ticket in tickets:
            if ticket["ticket_id"] == ticket_id:
                return ticket

        return None

    def update_ticket_status(self, ticket_id, status):
        """
        Update the status of a support ticket.
        """

        if status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Use one of: {VALID_STATUSES}"
            )

        tickets = self.get_all_tickets()

        for ticket in tickets:
            if ticket["ticket_id"] == ticket_id:
                ticket["status"] = status

                with open(
                    TICKETS_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        tickets,
                        file,
                        indent=2,
                        ensure_ascii=False
                    )

                return ticket

        return None