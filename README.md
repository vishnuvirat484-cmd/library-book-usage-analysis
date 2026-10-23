# Library Book Usage Analysis System

Python + MySQL circulation tracker with pandas/NumPy/Matplotlib analytics.

## Features
- Book & borrower records
- Issue / return with validation (no returns before issue, no double returns, no issue without copies)
- Configurable due date (`LOAN_PERIOD_DAYS` in `.env`)
- Most-borrowed books, overdue list, monthly circulation chart, category summary

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit DB_PASSWORD
python main.py init-db
python main.py seed-demo        # optional demo data
python main.py report
python main.py menu
pytest
```
Outputs are written to `reports/`.
