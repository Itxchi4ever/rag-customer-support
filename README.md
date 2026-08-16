# RAG Customer Support System

An AI-powered customer support system built using Retrieval-Augmented
Generation (RAG).

The application allows users to ask questions about TechNova products,
retrieve relevant information from a product knowledge base, generate
contextual answers using a Hugging Face language model, maintain
conversational context, and create and manage support tickets.

## Live Demo

Frontend: https://rag-customer-support.vercel.app/

Backend API: https://rag-customer-support-production.up.railway.app/

Health Check:
https://rag-customer-support-production.up.railway.app/health

> Note: The Railway backend may be temporarily unavailable when the
> production deployment is stopped to control resource usage.

## Features

-   AI-powered customer support
-   Retrieval-Augmented Generation
-   FAISS semantic retrieval
-   BM25 keyword retrieval
-   Hybrid retrieval
-   Conversational memory
-   Product-aware support
-   Support ticket creation and management
-   Ticket status updates
-   React frontend
-   FastAPI backend
-   Docker and Docker Compose support
-   Railway backend deployment
-   Vercel frontend deployment

## Architecture

``` text
User
 |
 v
React Frontend (Vercel)
 |
 | HTTPS
 v
FastAPI Backend (Railway + Docker)
 |
 v
Conversation Manager
 |
 v
RAG Pipeline
 |
 +-------------------+
 |                   |
 v                   v
FAISS              BM25
Semantic Search    Keyword Search
 |                   |
 +---------+---------+
           |
           v
   Relevant Context
           |
           v
   Hugging Face LLM
           |
           v
    Generated Answer
```

## RAG Pipeline

1.  Load product documents from the knowledge base.
2.  Split documents into smaller overlapping chunks.
3.  Generate embeddings for the chunks.
4.  Store and search embeddings using FAISS.
5.  Perform keyword retrieval using BM25.
6.  Combine relevant retrieval results.
7.  Construct context for the language model.
8.  Generate a grounded response using a Hugging Face model.

## Knowledge Base

The knowledge base is designed around TechNova products, including:

-   Techbook
-   Techbuds
-   Smartwatch

Additional product documentation can be added to extend the system.

## Tech Stack

### Frontend

-   React
-   Vite
-   JavaScript
-   CSS

### Backend

-   Python
-   FastAPI
-   Uvicorn
-   Pydantic

### AI and Retrieval

-   Hugging Face
-   Sentence Transformers
-   FAISS
-   BM25
-   LangChain text splitting utilities

### Document Processing

-   PyMuPDF

### Deployment

-   Docker
-   Docker Compose
-   Railway
-   Vercel

### Version Control

-   Git
-   GitHub

## Project Structure

``` text
rag-customer-support/
|
├── api/
│   └── main.py
├── chatbot/
│   ├── conversation.py
│   └── ticket_manager.py
├── llm/
│   ├── generator.py
│   └── rag.py
├── retrieval/
│   └── ...
├── ingestion/
│   └── ...
├── data/
│   └── ...
├── vectorstore/
│   └── ...
├── frontend/
│   └── react-app/
│       ├── src/
│       │   ├── App.jsx
│       │   ├── App.css
│       │   └── ...
│       ├── package.json
│       ├── vite.config.js
│       └── index.html
├── Dockerfile
├── docker-compose.yaml
├── .dockerignore
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

### Prerequisites

Install:

-   Python 3.13
-   Node.js
-   npm
-   Git
-   Docker Desktop (optional)

### Clone the Repository

``` bash
git clone https://github.com/Itxchi4ever/rag-customer-support.git
cd rag-customer-support
```

### Backend Setup

Create a virtual environment:

``` bash
python -m venv venv
```

Windows:

``` cmd
venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

``` env
HF_TOKEN=your_huggingface_token
FRONTEND_URL=http://localhost:5173
```

Start FastAPI:

``` bash
uvicorn api.main:app --reload --port 8000
```

Backend:

``` text
http://127.0.0.1:8000
```

Health check:

``` text
http://127.0.0.1:8000/health
```

Expected response:

``` json
{
  "status": "healthy"
}
```

### Frontend Setup

Navigate to the React application:

``` bash
cd frontend/react-app
```

Install dependencies:

``` bash
npm install
```

Create `frontend/react-app/.env`:

``` env
VITE_API_URL=http://127.0.0.1:8000
```

Start Vite:

``` bash
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

## Docker

Build the backend image:

``` bash
docker build -t rag-customer-support-api .
```

Run it:

``` bash
docker run --env-file .env -p 8000:8000 rag-customer-support-api
```

## Docker Compose

Start:

``` bash
docker compose up
```

Run in detached mode:

``` bash
docker compose up -d
```

Stop:

``` bash
docker compose down
```

## API Endpoints

### GET `/`

Basic API status endpoint.

### GET `/health`

Health check endpoint.

### POST `/chat`

Send a customer support question.

Example:

``` json
{
  "message": "My Techbuds are not connecting to Bluetooth."
}
```

### GET `/conversation`

Retrieve conversation information.

### DELETE `/conversation`

Clear the current conversation.

### GET `/tickets`

Retrieve support tickets.

### GET `/tickets/{ticket_id}`

Retrieve a specific ticket.

### PATCH `/tickets/{ticket_id}/status`

Update a ticket status.

Example:

``` json
{
  "status": "in_progress"
}
```

Supported statuses:

``` text
open
in_progress
resolved
```

## Environment Variables

Backend:

``` env
HF_TOKEN=your_huggingface_token
FRONTEND_URL=http://localhost:5173
```

Production backend configuration:

``` env
FRONTEND_URL=https://rag-customer-support.vercel.app
```

Frontend:

``` env
VITE_API_URL=http://127.0.0.1:8000
```

Production:

``` env
VITE_API_URL=https://rag-customer-support-production.up.railway.app
```

Never expose `HF_TOKEN` to the frontend.

Do not commit `.env` files.

Recommended `.gitignore` entries:

``` gitignore
.env
venv/
__pycache__/
*.pyc
node_modules/
frontend/react-app/dist/
```

## Production Deployment

### Backend

The FastAPI backend is containerized with Docker and deployed to
Railway.

Production URL:

https://rag-customer-support-production.up.railway.app/

### Frontend

The React frontend is deployed to Vercel.

Production URL:

https://rag-customer-support.vercel.app/

The frontend uses:

``` env
VITE_API_URL=https://rag-customer-support-production.up.railway.app
```

## Example Queries

``` text
My Techbuds are not connecting to Bluetooth.
```

``` text
How do I reset my smartwatch?
```

``` text
My Techbook is not turning on.
```

``` text
What should I do if my device is not charging?
```

## Conversational Memory

The application maintains conversation context so users can ask
follow-up questions naturally.

Example:

``` text
User:
My smartwatch is not charging.

Assistant:
Check the charging connection and make sure the charging contacts are clean.

User:
What if that doesn't work?
```

The assistant can use the previous conversation to understand the
follow-up question.

## Support Ticket System

Tickets contain:

``` text
Ticket ID
Product
Issue
Status
Created At
```

Supported ticket statuses:

``` text
open
in_progress
resolved
```

The frontend includes a ticket dashboard for viewing, refreshing, and
updating tickets.

## Development Workflow

``` text
Project Setup
    |
Document Ingestion
    |
Recursive Text Chunking
    |
Metadata
    |
Embeddings
    |
FAISS Vector Search
    |
Basic Retrieval
    |
RAG Generation
    |
Conversational Memory
    |
Customer Support Features
    |
Ticket Management
    |
FastAPI
    |
React Frontend
    |
Docker
    |
Docker Compose
    |
Railway Deployment
    |
Vercel Deployment
```

## Testing

Test the backend with:

``` text
GET /health
```

Test chat with:

``` text
POST /chat
```

Test the frontend at:

https://rag-customer-support.vercel.app/

Test:

-   Chat functionality
-   Conversation clearing
-   Ticket dashboard
-   Ticket refresh
-   Ticket status updates

## Performance

A chat request may perform several computationally intensive operations:

-   Query embedding
-   Vector retrieval
-   Keyword retrieval
-   Context construction
-   Language model inference

Performance depends on CPU, memory, model size, and deployment
environment.

## Future Improvements

-   Streaming LLM responses
-   Faster model inference
-   Retrieval reranking
-   Improved hybrid retrieval weighting
-   Persistent conversation storage
-   PostgreSQL integration
-   Persistent ticket database
-   User authentication
-   Admin authentication
-   Role-based access control
-   Redis caching
-   API rate limiting
-   Centralized logging
-   Automated RAG evaluation
-   Retrieval quality evaluation
-   Response quality evaluation
-   Automated tests
-   CI/CD pipeline
-   Improved mobile responsiveness
-   Advanced ticket analytics
-   Production observability

## Learning Outcomes

This project demonstrates practical experience with:

-   Python
-   FastAPI
-   REST APIs
-   React
-   Vite
-   JavaScript
-   RAG
-   Large Language Models
-   Hugging Face
-   Embeddings
-   Sentence Transformers
-   FAISS
-   BM25
-   Hybrid Retrieval
-   Conversational AI
-   Text Chunking
-   Document Processing
-   Docker
-   Docker Compose
-   Environment Variables
-   CORS
-   Git
-   GitHub
-   Railway
-   Vercel
-   Cloud Deployment

## Repository

https://github.com/Itxchi4ever/rag-customer-support

## Author

Shukla Harsh Jatashankar

GitHub:

https://github.com/Itxchi4ever
