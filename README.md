# PingMe Backend

FastAPI-based backend for PingMe, a real-time chat application with WebSocket support.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **User Registration**: Email and username validation
- **Room Management**: Create, list, and delete chat rooms
- **Real-time Chat**: WebSocket support for instant messaging
- **Typing Indicators**: Real-time typing status updates
- **Message History**: Persistent message storage and retrieval

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (with SQLite for testing)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **WebSockets**: FastAPI WebSocket support
- **Migrations**: Alembic
- **Testing**: pytest, httpx, pytest-asyncio

## Prerequisites

- Python 3.11+
- PostgreSQL 15+ (or use Docker)
- pip

## Installation

1. **Clone the repository**
   ```bash
   cd PingMe_Backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://pingme_user:pingme_pass@localhost:5432/chatapp
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Set up database**
   
   Make sure PostgreSQL is running, then run migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Using Docker

```bash
docker-compose up --build
```

This will start both the backend and PostgreSQL database.

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info (protected)

### Rooms

- `POST /rooms/` - Create a new room (protected)
- `GET /rooms/` - Get all rooms (protected)
- `GET /rooms/my-rooms` - Get rooms created by current user (protected)
- `DELETE /rooms/{room_id}` - Delete a room (protected)

### WebSocket

- `WS /ws/{room_id}` - Connect to chat room WebSocket

## Testing

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=app --cov-report=term-missing
```

Generate HTML coverage report:
```bash
pytest --cov=app --cov-report=html
```

### Test Coverage

- **Authentication Tests**: User registration, login, protected endpoints
- **Room Tests**: Room CRUD operations, authorization checks
- **Current Coverage**: 82%

See `app/tests/README.md` for detailed testing documentation.

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Project Structure

```
PingMe_Backend/
├── app/
│   ├── auth/              # Authentication utilities
│   ├── dependencies/      # FastAPI dependencies
│   ├── models/            # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   ├── routers/           # API route handlers
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── tests/             # Test suite
│   ├── utils/             # Utility functions
│   ├── websocket/         # WebSocket connection manager
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   └── main.py            # FastAPI application
├── alembic/               # Database migrations
├── docker-compose.yml     # Docker configuration
├── Dockerfile             # Docker image definition
├── pytest.ini             # Pytest configuration
└── requirements.txt       # Python dependencies
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |

## Development

### Code Style

The project follows Python PEP 8 style guidelines. Consider using:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

### Adding New Features

1. Create database model in `app/models/`
2. Create Pydantic schema in `app/schemas/`
3. Add repository methods in `app/repositories/`
4. Implement service logic in `app/services/`
5. Create router endpoints in `app/routers/`
6. Write tests in `app/tests/`
7. Create migration if needed: `alembic revision --autogenerate`

## License

This project is part of the PingMe application.

