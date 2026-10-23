"""Library Book Usage Analysis System - command line entry point.

Usage:
    python main.py init-db        # create schema + sample books/borrowers
    python main.py seed-demo      # generate demo loans for analytics
    python main.py menu           # interactive menu (default)
    python main.py report         # print reports, save charts + CSVs
"""
import argparse
from datetime import datetime

from config import REPORT_DIR, SQL_DIR, LOAN_PERIOD_DAYS
from library import books, borrowers, loans
from library.db import run_sql_file
from library.errors import LibraryError


def parse_date(text):
    text = text.strip()
    return datetime.strptime(text, "%Y-%m-%d").date() if text else None


def show(rows):
    if not rows:
        print("  (no records)")
        return
    for r in rows:
        print("  " + " | ".join(f"{k}={v}" for k, v in r.items()))


def init_db():
    run_sql_file(SQL_DIR / "schema.sql")
    run_sql_file(SQL_DIR / "seed.sql")
    print("Database initialised with sample books and borrowers.")


def seed_demo():
    from library.seed_demo import generate
    print(f"Created {generate()} demo loans.")


def report():
    from analytics import charts, reports
    df = reports.load_loans_df()
    if df.empty:
        print("No loans yet. Run: python main.py seed-demo")
        return
    REPORT_DIR.mkdir(exist_ok=True)

    top = reports.most_borrowed(df)
    monthly = reports.monthly_circulation(df)
    overdue = reports.overdue_loans(df)
    cats = reports.category_summary(df)

    print("\n== Summary ==");            print(reports.summary(df))
    print("\n== Most borrowed books =="); print(top.to_string(index=False))
    print("\n== Overdue loans ==");       print(overdue.to_string(index=False) if len(overdue) else "None")
    print("\n== Category summary ==");    print(cats.to_string(index=False))
    print("\n== Loan duration stats (days) =="); print(reports.loan_duration_stats(df))

    top.to_csv(REPORT_DIR / "most_borrowed.csv", index=False)
    overdue.to_csv(REPORT_DIR / "overdue_loans.csv", index=False)
    cats.to_csv(REPORT_DIR / "category_summary.csv", index=False)
    monthly.to_csv(REPORT_DIR / "monthly_circulation.csv", index=False)
    paths = [charts.plot_popular_books(top), charts.plot_monthly_trend(monthly),
             charts.plot_category_summary(cats)]
    print("\nSaved charts/CSVs in:", REPORT_DIR)
    for p in paths:
        print("  -", p.name)


def menu():
    options = """
===== Library Usage Analysis =====
1. Add book            6. Active loans
2. Add borrower        7. Overdue loans
3. Issue book          8. Generate reports & charts
4. Return book         9. Check copy-count consistency
5. List books          0. Exit
"""
    while True:
        print(options)
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                bid = books.add_book(input("ISBN: "), input("Title: "), input("Author: "),
                                     input("Category: "), int(input("Copies: ")))
                print("Added book id", bid)
            elif choice == "2":
                print("Added borrower id", borrowers.add_borrower(input("Name: "), input("Roll no: ")))
            elif choice == "3":
                d = parse_date(input("Issue date YYYY-MM-DD (blank = today): "))
                lid = loans.issue_book(int(input("Book id: ")), int(input("Borrower id: ")), issue_date=d)
                print(f"Loan {lid} created (due in {LOAN_PERIOD_DAYS} days by default).")
            elif choice == "4":
                lid = int(input("Loan id: "))
                d = parse_date(input("Return date YYYY-MM-DD (blank = today): "))
                print(loans.return_book(lid, return_date=d))
            elif choice == "5":
                show(books.list_books())
            elif choice == "6":
                show(loans.list_active_loans())
            elif choice == "7":
                show(loans.list_overdue_loans())
            elif choice == "8":
                report()
            elif choice == "9":
                bad = loans.check_consistency()
                print("All copy counts are consistent." if not bad else bad)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except LibraryError as e:
            print("Rejected:", e)
        except ValueError as e:
            print("Invalid input:", e)


def main():
    p = argparse.ArgumentParser(description="Library Book Usage Analysis System")
    p.add_argument("command", nargs="?", default="menu",
                   choices=["init-db", "seed-demo", "menu", "report"])
    cmd = p.parse_args().command
    {"init-db": init_db, "seed-demo": seed_demo, "menu": menu, "report": report}[cmd]()


if __name__ == "__main__":
    main()
