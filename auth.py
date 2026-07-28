"""
auth.py
=======
Authentication logic for the Travel Recommendation System.

Handles:
    - Password hashing and verification (bcrypt).
    - Input validation (email format, password strength, matching confirmation).
    - User registration and login, backed by database.DatabaseManager.

This module deliberately has NO Streamlit imports, so it can be unit
tested or reused outside a Streamlit context.
"""

import re
import bcrypt
from typing import Tuple, Optional, Dict, Any

from database import db


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
MIN_PASSWORD_LENGTH = 8


def is_valid_email(email: str) -> bool:
    """
    Check whether a string is a syntactically valid email address.

    Args:
        email: The email string to validate.

    Returns:
        True if the email matches a standard email pattern.
    """
    return bool(EMAIL_REGEX.match(email.strip()))


def is_strong_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.

    Rules enforced:
        - At least 8 characters long.
        - Contains at least one digit.
        - Contains at least one uppercase letter.

    Args:
        password: The plaintext password to check.

    Returns:
        A tuple of (is_valid, message). If is_valid is False, message
        explains what requirement was not met.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    return True, "Password is strong."


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt with a randomly generated salt.

    Args:
        password: The plaintext password.

    Returns:
        The bcrypt hash, decoded to a UTF-8 string for storage in SQLite
        (which stores it as TEXT).
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored bcrypt hash.

    Args:
        password: The plaintext password entered by the user.
        hashed_password: The bcrypt hash retrieved from the database.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except (ValueError, AttributeError):
        # Handles malformed/corrupted hashes gracefully instead of crashing.
        return False


# ---------------------------------------------------------------------------
# High-level auth operations
# ---------------------------------------------------------------------------

def register_user(
    full_name: str,
    email: str,
    password: str,
    confirm_password: str,
) -> Tuple[bool, str]:
    """
    Validate inputs and register a new user.

    Args:
        full_name: The user's full name.
        email: The user's email address.
        password: The chosen plaintext password.
        confirm_password: Re-entered password for confirmation.

    Returns:
        A tuple of (success, message) describing the outcome, suitable
        for direct display in the Streamlit UI.
    """
    full_name = full_name.strip()
    email = email.strip().lower()

    # --- Basic field checks ---
    if not full_name:
        return False, "Full name is required."
    if not email:
        return False, "Email is required."
    if not is_valid_email(email):
        return False, "Please enter a valid email address."
    if password != confirm_password:
        return False, "Passwords do not match."

    strong_enough, strength_message = is_strong_password(password)
    if not strong_enough:
        return False, strength_message

    # --- Duplicate email check ---
    if db.email_exists(email):
        return False, "An account with this email already exists. Please log in instead."

    # --- Persist the user ---
    hashed = hash_password(password)
    success = db.add_user(full_name=full_name, email=email, hashed_password=hashed)

    if success:
        return True, "Registration successful! You can now log in."
    return False, "Something went wrong while registering. Please try again."


def login_user(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Validate credentials and log a user in.

    Args:
        email: The email address entered by the user.
        password: The plaintext password entered by the user.

    Returns:
        A tuple of (success, message, user_data). user_data is a dict
        with keys (id, full_name, email, created_at) on success, or
        None on failure.
    """
    email = email.strip().lower()

    if not email or not password:
        return False, "Please enter both email and password.", None

    user = db.get_user_by_email(email)
    if user is None:
        return False, "No account found with this email.", None

    if not verify_password(password, user["password"]):
        return False, "Incorrect password. Please try again.", None

    # Don't leak the password hash back to the caller/UI layer.
    safe_user_data = {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }
    return True, f"Welcome back, {user['full_name']}!", safe_user_data
