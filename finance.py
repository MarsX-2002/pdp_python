import sys
import sqlite3
from prettytable import PrettyTable


class FinanceRepo:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS finance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    earn REAL,
                    spend REAL
                )
                """
            )

    def earn(self, income):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO finance (earn)
                VALUES (?)
                """,
                (income,)
            )

    def spend(self, cost):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO finance (spend)
                VALUES (?)
                """,
                (cost,)
            )

    def balance(self):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute(
                """
                SELECT COALESCE(SUM(earn), 0) - COALESCE(SUM(spend), 0) AS balance 
                FROM finance
                """
            )
            return cursor.fetchall()

    def pretty_print(self, data):
        table = PrettyTable()
        table.field_names = ["Balance"]
        for row in data:
            table.add_row(row)
        print(table)


def main():
    db_path = r'/home/kingcode/Desktop/pdp_python/advanced/sqlite/finance.db'

    try:
        with sqlite3.connect(db_path) as db:
            repo = FinanceRepo(db)

            if len(sys.argv) < 2:
                sys.exit("At least 2 arguments required")

            available_commands = ('spend', 'earn', 'balance')
            command = sys.argv[1]

            if command not in available_commands:
                sys.exit(f"Unknown command: {command}, \nAvailable commands: {available_commands}")

            if command == 'earn':
                if len(sys.argv) != 3:
                    sys.exit("Amount required for earning")
                income = sys.argv[2]
                repo.earn(income)
                print("Money successfully earned!")

            elif command == 'spend':
                if len(sys.argv) != 3:
                    sys.exit("Amount required for spending")
                cost = sys.argv[2]
                repo.spend(cost)
                print("Money successfully spent!")

            elif command == 'balance':
                balance = repo.balance()
                repo.pretty_print(balance)

    except sqlite3.Error as e:
        sys.exit(f"SQLite error: {e}")


if __name__ == '__main__':
    main()
