import os
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from chatbot.conversation import Conversation
from chatbot.ticket_manager import TicketManager


# Load environment variables from .env
load_dotenv()


app = FastAPI(
    title="RAG Customer Support API",
    description="Customer support API powered by conversational RAG.",
    version="1.0.0"
)


# --------------------------------------------------
# CORS configuration
# --------------------------------------------------

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

origins = [
    frontend_url,
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Application state
# --------------------------------------------------

chatbot = Conversation()
ticket_manager = TicketManager()


# --------------------------------------------------
# Request models
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str


class TicketStatusRequest(BaseModel):
    status: Literal[
        "open",
        "in_progress",
        "resolved"
    ]


# --------------------------------------------------
# Basic endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "RAG Customer Support API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Chat endpoint
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    answer = chatbot.chat(request.message)

    ticket = chatbot.get_last_ticket()

    response = {
        "answer": answer,
        "ticket": ticket
    }

    return response


# --------------------------------------------------
# Conversation
# --------------------------------------------------

@app.get("/conversation")
def get_conversation():

    return {
        "history": chatbot.get_history()
    }


@app.delete("/conversation")
def clear_conversation():

    chatbot.clear_history()

    return {
        "message": "Conversation cleared"
    }


# --------------------------------------------------
# Tickets
# --------------------------------------------------

@app.get("/tickets")
def get_tickets():

    return {
        "tickets": ticket_manager.get_all_tickets()
    }


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):

    ticket = ticket_manager.get_ticket(ticket_id)

    if not ticket:
        return {
            "error": "Ticket not found"
        }

    return ticket


@app.patch("/tickets/{ticket_id}/status")
def update_ticket_status(
    ticket_id: str,
    request: TicketStatusRequest
):

    ticket = ticket_manager.update_ticket_status(
        ticket_id,
        request.status
    )

    if not ticket:
        return {
            "error": "Ticket not found"
        }

    return ticket