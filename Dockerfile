# Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app ./app
COPY alembic.ini .
COPY ./alembic ./alembic

# Expose port
EXPOSE $PORT

# Run migrations and start app
CMD sh -c "echo 'Running database migrations...' && alembic upgrade head && echo 'Migrations completed. Starting server...' && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"