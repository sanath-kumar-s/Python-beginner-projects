# database/db_manager.py
import sqlite3
import os
from .schema import CREATE_CATEGORIES_TABLE, CREATE_EXPENSES_TABLE, DEFAULT_CATEGORIES

class DatabaseManager:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_CATEGORIES_TABLE)
            cursor.execute(CREATE_EXPENSES_TABLE)
            
            # Insert default categories if none exist
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                for category in DEFAULT_CATEGORIES:
                    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))
            conn.commit()

    def execute_query(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetch_all(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
