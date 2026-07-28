import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime

DB_FOLDER = "database"
DB_NAME = "users.db"

os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, DB_NAME)


class Database:

    def __init__(self):
        self.create_tables()

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        try:
            yield conn
            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    def create_tables(self):

        query = """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
        """

        with self.connection() as conn:
            conn.execute(query)

    ##########################################################
    # USER METHODS
    ##########################################################

    def create_user(self, full_name, email, password):

        try:

            with self.connection() as conn:

                conn.execute(
                    """
                    INSERT INTO users
                    (full_name,email,password,created_at)

                    VALUES(?,?,?,?)
                    """,
                    (
                        full_name.strip(),
                        email.lower().strip(),
                        password,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                )

            return True

        except sqlite3.IntegrityError:
            return False

    def email_exists(self, email):

        with self.connection() as conn:

            cur = conn.execute(

                "SELECT id FROM users WHERE email=?",

                (email.lower().strip(),)

            )

            return cur.fetchone() is not None

    def get_user(self, email):

        with self.connection() as conn:

            cur = conn.execute(

                "SELECT * FROM users WHERE email=?",

                (email.lower().strip(),)

            )

            row = cur.fetchone()

            if row:

                return dict(row)

            return None

    def get_all_users(self):

        with self.connection() as conn:

            cur = conn.execute("""

                SELECT

                    id,

                    full_name,

                    email,

                    created_at

                FROM users

                ORDER BY id DESC

            """)

            return [dict(x) for x in cur.fetchall()]


db = Database()
