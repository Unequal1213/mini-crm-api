# Mini CRM API

[![CI](https://github.com/Unequal1213/mini-crm-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Unequal1213/mini-crm-api/actions/workflows/ci.yml)

Mini CRM API is a production-style FastAPI backend for managing customers, deals,
sales pipeline stages, and CRM statistics. It is built as a portfolio project to
demonstrate clean backend API design, relational data modeling, CRUD workflows,
filtering, sorting, testing, Docker, and GitHub Actions CI.

## Features

- Health check endpoint for service monitoring.
- Customer CRUD endpoints.
- Deal CRUD endpoints linked to customer records.
- Deal pagination, filtering, and sorting.
- Sales pipeline statistics endpoint.
- PostgreSQL database support with SQLAlchemy ORM.
- Alembic migrations for database schema management.
- Docker Compose setup for local API and PostgreSQL services.
- Pytest test suite using in-memory SQLite for fast local tests.
- Ruff linting.
- GitHub Actions CI for every push and pull request.

## Tech Stack

- Python 3.13
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker and Docker Compose
- Pytest
- Ruff
- GitHub Actions

## Project Structure

```text
app/
  api/          FastAPI route modules
  database/     Database engine, session, and base model setup
  models/       SQLAlchemy models
  schemas/      Pydantic request and response schemas
  services/     Business logic used by API routes
  main.py       FastAPI application entry point
alembic/
  versions/     Database migration files
tests/          Pytest test suite
```

## Environment Variables

Create a local `.env` file from the example file:

```bash
cp .env.example .env
```

The `.env.example` file contains placeholder values only:

```text
DATABASE_URL=postgresql+psycopg://mini_crm_user:mini_crm_password@postgres:5432/mini_crm
POSTGRES_USER=mini_crm_user
POSTGRES_PASSWORD=mini_crm_password
POSTGRES_DB=mini_crm
```

Do not commit real secrets or production credentials.

## Docker Setup

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

Stop the containers:

```bash
docker compose down
```

Remove the PostgreSQL volume if you want a fresh local database:

```bash
docker compose down -v
```

## Local Development Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

For local development without Docker, set `DATABASE_URL` to a PostgreSQL database
that is reachable from your machine.

Run the app:

```bash
python -m uvicorn app.main:app --reload
```

## Database Migrations

Run migrations:

```bash
python -m alembic upgrade head
```

Create a new migration after changing models:

```bash
python -m alembic revision --autogenerate -m "describe change"
```

Show the current migration state:

```bash
python -m alembic current
```

## Testing

Run the test suite:

```bash
python -m pytest
```

Tests use an in-memory SQLite database and do not require a running PostgreSQL
server.

## Linting

Run Ruff:

```bash
python -m ruff check .
```

## API Endpoints

### Health

- `GET /health` returns the application health status.

### Customers

- `POST /customers` creates a customer.
- `GET /customers` lists customers.
- `GET /customers/{customer_id}` returns one customer.
- `PATCH /customers/{customer_id}` updates provided customer fields.
- `DELETE /customers/{customer_id}` deletes a customer.

### Deals

- `POST /deals` creates a deal linked to an existing customer.
- `GET /deals` lists deals.
- `GET /deals/{deal_id}` returns one deal.
- `PATCH /deals/{deal_id}` updates provided deal fields.
- `DELETE /deals/{deal_id}` deletes a deal.

## Deal Filtering And Sorting

`GET /deals` supports pagination, filtering, and sorting with query parameters:

- `limit`: number of results to return, from `1` to `100`, default `20`.
- `offset`: number of results to skip, minimum `0`, default `0`.
- `stage`: filter by `lead`, `qualified`, `proposal`, `won`, or `lost`.
- `customer_id`: filter deals by customer.
- `source`: filter deals by source.
- `min_value`: filter deals with value greater than or equal to this amount.
- `max_value`: filter deals with value less than or equal to this amount.
- `sort_by`: one of `expected_close_date`, `created_at`, `updated_at`,
  `value`, `title`, `stage`, or `source`.
- `sort_order`: `asc` or `desc`.

Default sorting is `created_at desc`.

Example:

```bash
curl "http://localhost:8000/deals?stage=proposal&sort_by=value&sort_order=desc"
```

## Sales Pipeline Statistics

`GET /deals/stats` returns CRM pipeline analytics:

- `total`
- `lead`
- `qualified`
- `proposal`
- `won`
- `lost`
- `total_value`
- `won_value`
- `open_value`

Open value includes deals in `lead`, `qualified`, and `proposal` stages.

## Continuous Integration

GitHub Actions runs on every push and pull request. The CI workflow uses Python
3.13, installs `requirements-dev.txt`, runs Ruff, and runs Pytest:

```bash
python -m ruff check .
python -m pytest
```
