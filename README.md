# 🚀 PingMe Backend API

**PingMe** is a lightning-fast, real-time chat backend built with **FastAPI**.  
It’s designed for modern web apps that need speed, scalability, and clean architecture — powered by async Python, PostgreSQL, and Redis.

---

## What Makes It Awesome

- **Clean Architecture** — Repository + Service pattern for maintainable, testable code.
- **Asynchronous Everything** — FastAPI + SQLAlchemy 2.0 async stack for crazy fast I/O and concurrency.
- **Secure Auth System** — JWT-based authentication with both Access and Refresh tokens.
- **Real-Time Messaging** — WebSockets + Redis Pub/Sub for instant message delivery.
- **Containerized Setup** — Docker + Docker Compose for a zero-hassle development environment.

---

## 🛠 Tech Stack

| Category | Technology | Purpose |
|-----------|-------------|----------|
| **Framework** | FastAPI | High-performance async web framework |
| **Database** | PostgreSQL | Persistent relational database (users, rooms, messages) |
| **ORM** | SQLAlchemy 2.0 (async) | Modern async ORM layer |
| **Broker** | Redis | Handles WebSocket events and Pub/Sub messaging |
| **Security** | JWT, Passlib, python-jose | Token management + bcrypt hashing |
| **Deployment** | Docker, Docker Compose | Containerization and orchestration |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python **3.11+**
- **Docker** and **Docker Compose**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/pingme-backend.git
cd pingme-backend



-Access the App

Swagger Docs: http://localhost:8000/docs

Root Endpoint: http://localhost:8000/
