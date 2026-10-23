"""Central configuration. Values come from environment variables / .env file."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv is optional for unit tests
    pass

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
SQL_DIR = BASE_DIR / "sql"

DB_NAME = os.getenv("DB_NAME", "library_db")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": DB_NAME,
}

# Configurable due-date rule: due_date = issue_date + LOAN_PERIOD_DAYS
LOAN_PERIOD_DAYS = int(os.getenv("LOAN_PERIOD_DAYS", "14"))
