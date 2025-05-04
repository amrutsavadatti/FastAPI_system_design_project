from uuid import uuid4
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import text
from app.core.security import hash_password
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.services.profile import create_profile

# from utils.security import hash_password  # assuming you're hashing passwords

async def create_user_account(db: Session, email: EmailStr, password: str):
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

        result = db.execute(
            text("""
                INSERT INTO users (user_id, email, hashed_password, role, is_active, created_at)
                VALUES (:user_id, :email, :password, :role, :is_active, :created_at)
            """),
            {
                "user_id": user_id,
                "email": email,
                "password": hashed_pw,
                "role": "user",
                "is_active": True,
                "created_at": datetime.now(timezone.utc)
            }
        )

        status = await create_profile(user_id)
        if status["success"] == True:
            db.commit()
        else:
            raise HTTPException(status_code=500, detail="Profile not created")

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
            "error": str(e)
        }


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

