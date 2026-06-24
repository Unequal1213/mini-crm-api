# mini-crm-api
FastAPI backend service for managing customers, deals, sales pipeline stages, and CRM statistics.

## API

- `GET /health` returns the application health status.
- `POST /customers` creates a customer.
- `GET /customers` lists customers.
- `GET /customers/{customer_id}` returns one customer.
- `PATCH /customers/{customer_id}` updates provided customer fields.
- `DELETE /customers/{customer_id}` deletes a customer.

## Run with Docker

Create a local environment file from the example:

```bash
cp .env.example .env
```

The values in `.env.example` are placeholders for local development. Replace them
before using the project outside your machine.

Build and start the API with PostgreSQL:

```bash
docker compose up --build
```

The app service waits for PostgreSQL, runs Alembic migrations, and starts Uvicorn
on `http://localhost:8000`.

Check the health endpoint:

```bash
curl http://localhost:8000/health
```
