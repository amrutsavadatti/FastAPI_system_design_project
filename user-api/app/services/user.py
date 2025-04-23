from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import text

from app.core.security import hash_password
from app.db.fake_users import users_db
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from sqlalchemy import text
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import EmailStr

# from utils.security import hash_password  # assuming you're hashing passwords


def create_user_account(db: Session, email: EmailStr, password: str):
    try:
        # Reuse existing email check function
        result = get_user_by_email(db, str(email))

        if result["exists"]:
            return {
                "created": False,
                "data": None,
                "message": "User already exists"
            }

        user_id = str(uuid4())
        hashed_pw = hash_password(password)

        db.execute(
            text("""
                INSERT INTO users (email, hashed_password, role, is_active, created_at)
                VALUES (:email, :password, :role, :is_active, :created_at)
            """),
            {
                "email": email,
                "password": hashed_pw,
                "role": "user",
                "is_active": True,
                "created_at": datetime.now(timezone.utc)
            }
        )
        db.commit()

        return {
            "created": True,
            "data": {
                "id": user_id,
                "email": email
            }
        }

    except Exception as e:
        db.rollback()
        print(f"[ERROR] create_user_account: {e}")
        return {
            "created": False,
            "data": None,
            "error": "Database error"
        }


# def create_user_account(username: str, email: EmailStr, password: str):
#     user_id = str(uuid4())
#     users_db[user_id] = {
#         "id": user_id,
#         "username": username,
#         "email": email,
#         "hashed_password": hash_password(password),
#         "created_at": datetime.now(timezone.utc),
#         "is_active": True
#     }
#     return users_db[user_id]


def get_user_by_email(db: Session, email: str):
    try:
        print("inside function")

        row = db.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        ).mappings().fetchone()

        if row:
            user_data = dict(row)
            return {
                "exists": True,
                "data": user_data
            }
        else:
            return {
                "exists": False,
                "data": None
            }

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return {
            "exists": False,
            "data": str(e),
            "error": "Database query failed"
        }

# def get_user_by_email(db: Session, email: str):
#
#     print("inside function")
#     row = db.execute(text("SELECT * FROM users WHERE email = :email"),{"email": email}).mappings().fetchone()
#     print(type(row))
#     diction = dict(row)
#     print(diction)
#     return True
    # return next((u for u in users_db.values() if u["email"] == email), None)

# def get_user_by_username(username: str):
#     return next((u for u in users_db.values() if u["username"] == username), None)

