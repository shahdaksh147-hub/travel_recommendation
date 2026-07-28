"""
database.py
============
Handles all SQLite database operations for the Travel Recommendation System.

This module is intentionally the ONLY place in the project that talks to
SQLite directly. Every other module (auth.py, pages/*) should go through
the DatabaseManager class defined here.
"""

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, Dict, Any


# Path to the SQLite database file. Kept in its own "database" folder
# as specified in the project structure.
DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "users.db")


class DatabaseManager:
    """
    Manages the SQLite connection and all queries related to the
    `users` table.

    Responsibilities:
        - Ensure the database file and folder exist.
        - Create the `users` table if it doesn't already exist.
        - Provide safe, reusable methods for inserting and fetching users.
    """

    def __init__(self, db_path: str = DB_PATH) -> None:
        """
        Initialize the DatabaseManager.

        Args:
            db_path: Path to the SQLite database file. Defaults to
                     'database/users.db'.
        """
        self.db_path = db_path
        self._ensure_db_directory_exists()
        self._create_tables()

    def _ensure_db_directory_exists(self) -> None:
        """Create the database directory if it does not already exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    @contextmanager
    def get_connection(self):
        """
        Context manager that yields a SQLite connection and guarantees
        it is closed afterwards, even if an error occurs.

        Yields:
            sqlite3.Connection: An open connection with row factory set
                                 so rows can be accessed like dictionaries.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _create_tables(self) -> None:
        """Create the `users` table if it does not already exist."""
        create_users_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """
        with self.get_connection() as conn:
            conn.execute(create_users_table_sql)

    def email_exists(self, email: str) -> bool:
        """
        Check whether a given email is already registered.

        Args:
            email: Email address to check.

        Returns:
            True if the email exists in the users table, False otherwise.
        """
        query = "SELECT 1 FROM users WHERE email = ? LIMIT 1;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (email.lower().strip(),))
            return cursor.fetchone() is not None

    def add_user(self, full_name: str, email: str, hashed_password: str) -> bool:
        """
        Insert a new user into the users table.

        Args:
            full_name: The user's full name.
            email: The user's email address (stored lowercase).
            hashed_password: A bcrypt-hashed password string.

        Returns:
            True if the user was added successfully, False if the email
            already exists or another error occurred.
        """
        if self.email_exists(email):
            return False

        insert_sql = """
            INSERT INTO users (full_name, email, password, created_at)
            VALUES (?, ?, ?, ?);
        """
        created_at = datetime.now().isoformat(timespec="seconds")

        try:
            with self.get_connection() as conn:
                conn.execute(
                    insert_sql,
                    (full_name.strip(), email.lower().strip(), hashed_password, created_at),
                )
            return True
        except sqlite3.IntegrityError:
            # Handles the rare race condition where email_exists() passed
            # but a duplicate was inserted concurrently.
            return False
        except sqlite3.Error as e:
            print(f"Database error while adding user: {e}")
            return False

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a single user's record by email.

        Args:
            email: Email address to look up.

        Returns:
            A dictionary with keys (id, full_name, email, password,
            created_at) if found, otherwise None.
        """
        query = "SELECT * FROM users WHERE email = ? LIMIT 1;"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (email.lower().strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_users(self) -> list:
        """
        Fetch all registered users (excluding password hashes for safety).

        Returns:
            A list of dictionaries, each containing id, full_name, email,
            and created_at.
        """
        query = "SELECT id, full_name, email, created_at FROM users ORDER BY created_at DESC;"
        with self.get_connection() as conn:
            cursor = conn.execute(query)
            return [dict(row) for row in cursor.fetchall()]


# A single shared instance other modules can import directly:
#   from database import db
db = DatabaseManager()
