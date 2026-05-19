Mini Logistics OMS - Backend

Quickstart

- Create a Python venv and install dependencies:

  python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt

- Configure Oracle DB via .env or environment variables matching keys in app/core/config.py (ORACLE_USER, ORACLE_PASSWORD, ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE)

- Run the app locally:

  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Notes

- This is an assessment-focused, production-style scaffold. Use Alembic for migrations in real deployments.
- Oracle is required to run the full application; tests use SQLite in-memory for service-level tests.
- JWT secret is set in defaults; override in environment for security.
