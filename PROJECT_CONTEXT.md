# PROJECT_CONTEXT.md

## Project

Mini CRM API

## Goal

Create a portfolio-ready backend project that demonstrates Python backend development, relational database modeling, CRUD operations, filtering, sorting, and sales pipeline statistics logic.

The application will help manage customers, deals, deal stages, sources, notes, expected close dates, and CRM statistics.

## Repository

GitHub repository:
https://github.com/Unequal1213/mini-crm-api

## Target role

Junior Python Backend Developer

## Planned stack

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

## Architecture direction

Use a clean and understandable structure:

- app/main.py
- app/api/
- app/models/
- app/schemas/
- app/services/
- app/database/

Business logic should live in app/services/ and should not be hardcoded inside API routes.

## Current status

Repository has just been created.

Next step:
Create the initial FastAPI project structure with health endpoint, dependencies, requirements, Ruff, Pytest, and basic CI-ready foundations.

## Important rules

- Do not commit .env.
- Do not hardcode secrets.
- Keep changes small and focused.
- Prefer clear code over clever abstractions.
- Tests should not require a real PostgreSQL database unless explicitly requested.
