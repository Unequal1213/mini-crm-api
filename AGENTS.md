# AGENTS.md

## Project context

This is a portfolio backend project for a self-taught Junior Python Backend Developer.

Project name:
Mini CRM API

Main goal:
Build a production-style FastAPI backend for managing customers, deals, sales pipeline stages, and CRM statistics.

The project should demonstrate:
- backend API design
- database modeling
- relational data
- CRUD workflows
- filtering and sorting
- sales pipeline statistics endpoint
- testing
- Docker
- GitHub Actions CI

## Tech stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker
- Pytest
- Ruff
- GitHub Actions

## Development rules

- Do not rewrite the entire project unless explicitly requested.
- Make small, focused changes.
- Explain every changed file.
- Preserve a clean FastAPI project structure.
- Use type hints.
- Follow PEP8.
- Avoid quick hacks.
- Do not commit secrets.
- Do not hardcode API keys, passwords, tokens, or database URLs.
- Use environment variables for configuration.
- Keep business logic separate from API routes.
- Prefer maintainable code over clever code.

## Initial MVP

Build a backend API for a small CRM system.

Core resources:
- Customer
- Deal

Customer fields:
- id
- name
- email
- phone
- company
- notes
- created_at
- updated_at

Deal fields:
- id
- customer_id
- title
- value
- stage
- source
- notes
- expected_close_date
- created_at
- updated_at

Allowed deal stages:
- lead
- qualified
- proposal
- won
- lost

Initial endpoints:
- GET /health
- POST /customers
- GET /customers
- GET /customers/{customer_id}
- PATCH /customers/{customer_id}
- DELETE /customers/{customer_id}
- POST /deals
- GET /deals
- GET /deals/{deal_id}
- PATCH /deals/{deal_id}
- DELETE /deals/{deal_id}
- GET /deals/stats

Stats endpoint should return:
- total
- lead
- qualified
- proposal
- won
- lost
- total_value
- won_value
- open_value

Open value should include deals in:
- lead
- qualified
- proposal

## Review guidelines

- Check for security issues.
- Check for hardcoded secrets.
- Check database session handling.
- Check API validation.
- Check test coverage.
- Check whether the code is understandable for a Junior Developer.
