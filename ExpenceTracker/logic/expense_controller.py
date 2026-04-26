# logic/expense_controller.py
from database.db_manager import DatabaseManager
from datetime import datetime

class ExpenseController:
    def __init__(self):
        self.db = DatabaseManager()

    def add_expense(self, amount, category, date, note):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        
        query = "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (amount, category, date, note))

    def get_expenses(self, start_date=None, end_date=None, category=None):
        query = "SELECT id, date, category, amount, note FROM expenses WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if category and category != "All":
            query += " AND category = ?"
            params.append(category)
            
        query += " ORDER BY date DESC"
        return self.db.fetch_all(query, tuple(params))

    def delete_expense(self, expense_id):
        query = "DELETE FROM expenses WHERE id = ?"
        self.db.execute_query(query, (expense_id,))

    def get_categories(self):
        query = "SELECT name FROM categories"
        rows = self.db.fetch_all(query)
        return [row[0] for row in rows]

    def add_category(self, name):
        query = "INSERT OR IGNORE INTO categories (name) VALUES (?)"
        self.db.execute_query(query, (name,))

    def delete_category(self, name):
        # Check if category is used in expenses
        check_query = "SELECT COUNT(*) FROM expenses WHERE category = ?"
        count = self.db.fetch_one(check_query, (name,))[0]
        if count > 0:
            raise ValueError(f"Category '{name}' is in use and cannot be deleted.")
        
        query = "DELETE FROM categories WHERE name = ?"
        self.db.execute_query(query, (name,))

    def get_category_distribution(self):
        query = "SELECT category, SUM(amount) FROM expenses GROUP BY category"
        return self.db.fetch_all(query)

    def get_spending_over_time(self):
        query = "SELECT date, SUM(amount) FROM expenses GROUP BY date ORDER BY date"
        return self.db.fetch_all(query)
