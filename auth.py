import re
import bcrypt

from database import db

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

MIN_PASSWORD_LENGTH = 8


# ---------------------------------------------------
# Validation
# ---------------------------------------------------

def validate_email(email):

    return re.match(EMAIL_REGEX, email) is not None


def validate_password(password):

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, "Password must contain at least 8 characters."

    if not any(c.isupper() for c in password):
        return False, "Password must contain one uppercase letter."

    if not any(c.isdigit() for c in password):
        return False, "Password must contain one number."

    return True, "OK"


# ---------------------------------------------------
# Password Hashing
# ---------------------------------------------------

def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):

    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


# ---------------------------------------------------
# Register
# ---------------------------------------------------

def register_user(full_name, email, password, confirm_password):

    full_name = full_name.strip()
    email = email.lower().strip()

    if full_name == "":
        return False, "Full name is required."

    if not validate_email(email):
        return False, "Enter a valid email."

    if password != confirm_password:
        return False, "Passwords do not match."

    ok, msg = validate_password(password)

    if not ok:
        return False, msg

    if db.email_exists(email):
        return False, "Email already registered."

    hashed = hash_password(password)

    if db.create_user(
        full_name,
        email,
        hashed
    ):
        return True, "Registration Successful."

    return False, "Unable to register."


# ---------------------------------------------------
# Login
# ---------------------------------------------------

def login_user(email, password):

    email = email.lower().strip()

    if email == "" or password == "":
        return False, "Please enter email and password.", None

    user = db.get_user(email)

    if user is None:
        return False, "User not found.", None

    if not verify_password(
        password,
        user["password"]
    ):
        return False, "Incorrect password.", None

    safe_user = {

        "id": user["id"],

        "full_name": user["full_name"],

        "email": user["email"],

        "created_at": user["created_at"]

    }

    return True, "Login Successful.", safe_user
