import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [showTickets, setShowTickets] = useState(false);
  const [tickets, setTickets] = useState([]);
  const [ticketsLoading, setTicketsLoading] = useState(false);

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: message,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from server");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);

      if (data.ticket) {
        loadTickets();
      }
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the support server.",
        },
      ]);

      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const clearConversation = async () => {
    try {
      await fetch(`${API_URL}/conversation`, {
        method: "DELETE",
      });

      setMessages([]);
    } catch (error) {
      console.error(error);
    }
  };

  const loadTickets = async () => {
    setTicketsLoading(true);

    try {
      const response = await fetch(`${API_URL}/tickets`);

      if (!response.ok) {
        throw new Error("Failed to load tickets");
      }

      const data = await response.json();

      setTickets(data.tickets || []);
    } catch (error) {
      console.error(error);
    } finally {
      setTicketsLoading(false);
    }
  };

  const toggleTickets = () => {
    if (!showTickets) {
      loadTickets();
    }

    setShowTickets((previous) => !previous);
  };

  const updateTicketStatus = async (ticketId, status) => {
    try {
      const response = await fetch(
        `${API_URL}/tickets/${ticketId}/status`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            status: status,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update ticket");
      }

      const updatedTicket = await response.json();

      setTickets((previous) =>
        previous.map((ticket) =>
          ticket.ticket_id === updatedTicket.ticket_id
            ? updatedTicket
            : ticket
        )
      );
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>TechNova Support</h1>
          <p>AI Customer Support Assistant</p>
        </div>

        <div className="header-actions">
          <button
            className="tickets-button"
            onClick={toggleTickets}
          >
            {showTickets ? "Back to Chat" : "Tickets"}
          </button>

          <button
            className="clear-button"
            onClick={clearConversation}
          >
            Clear Chat
          </button>
        </div>
      </header>

      {/* TICKET DASHBOARD */}
      {showTickets ? (
        <main className="tickets-container">

          <div className="tickets-header">
            <div>
              <h2>Support Tickets</h2>
              <p>
                Manage customer support requests
              </p>
            </div>

            <button
              className="refresh-button"
              onClick={loadTickets}
            >
              Refresh
            </button>
          </div>

          {ticketsLoading ? (
            <div className="empty-state">
              Loading tickets...
            </div>
          ) : tickets.length === 0 ? (
            <div className="empty-state">
              No support tickets found.
            </div>
          ) : (
            <div className="ticket-list">

              {tickets.map((ticket) => (
                <div
                  className="ticket-card"
                  key={ticket.ticket_id}
                >

                  <div className="ticket-top">

                    <div>
                      <h3>
                        {ticket.ticket_id}
                      </h3>

                      <span className="ticket-product">
                        {ticket.product}
                      </span>
                    </div>

                    <select
                      value={ticket.status}
                      onChange={(event) =>
                        updateTicketStatus(
                          ticket.ticket_id,
                          event.target.value
                        )
                      }
                      className={`status-select ${ticket.status}`}
                    >
                      <option value="open">
                        Open
                      </option>

                      <option value="in_progress">
                        In Progress
                      </option>

                      <option value="resolved">
                        Resolved
                      </option>
                    </select>

                  </div>

                  <p className="ticket-issue">
                    {ticket.issue}
                  </p>

                  <div className="ticket-date">
                    Created: {ticket.created_at}
                  </div>

                </div>
              ))}

            </div>
          )}

        </main>
      ) : (

        /* CHAT */
        <>
          <main className="chat-container">

            {messages.length === 0 ? (
              <div className="welcome">

                <div className="welcome-icon">
                  ✦
                </div>

                <h2>
                  How can I help you?
                </h2>

                <p>
                  Ask me about your TechNova products,
                  troubleshooting, setup, warranty, or returns.
                </p>

                <div className="suggestions">

                  <button
                    onClick={() =>
                      setInput(
                        "My Techbuds are not connecting to Bluetooth."
                      )
                    }
                  >
                    Techbuds connection problem
                  </button>

                  <button
                    onClick={() =>
                      setInput(
                        "How do I reset my smartwatch?"
                      )
                    }
                  >
                    Reset my smartwatch
                  </button>

                  <button
                    onClick={() =>
                      setInput(
                        "My Techbook is not turning on."
                      )
                    }
                  >
                    Techbook troubleshooting
                  </button>

                </div>

              </div>
            ) : (

              <div className="messages">

                {messages.map((message, index) => (

                  <div
                    key={index}
                    className={`message-row ${message.role}`}
                  >
                    <div className="message">
                      {message.content}
                    </div>
                  </div>

                ))}

                {loading && (
                  <div className="message-row assistant">
                    <div className="message loading">
                      Thinking...
                    </div>
                  </div>
                )}

              </div>

            )}

          </main>

          {/* INPUT */}
          <div className="input-area">

            <div className="input-wrapper">

              <textarea
                value={input}
                onChange={(event) =>
                  setInput(event.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Ask a question about your product..."
                rows="1"
                disabled={loading}
              />

              <button
                className="send-button"
                onClick={sendMessage}
                disabled={
                  loading || !input.trim()
                }
              >
                Send
              </button>

            </div>

            <p className="disclaimer">
              AI-generated responses are based on the
              TechNova knowledge base.
            </p>

          </div>
        </>
      )}

    </div>
  );
}

export default App;