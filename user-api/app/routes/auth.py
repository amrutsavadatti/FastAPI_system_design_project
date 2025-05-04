from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.user import UserSignup
from app.core.config import settings
from app.services.user import get_user_by_email, create_user_account
from app.core.security import verify_password
from app.utils.db import get_db
import requests

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSignup,  db: Session = Depends(get_db)):

    result = await create_user_account(db, user.email, user.password)
    if not result["created"]:
        raise HTTPException(status_code=500, detail=result)


    response = requests.post(settings.JWT_API_URL + "/jwt/token", json={
        "username": user.email,
        "password": user.password
    })

    if response.status_code != 200:
        return {"status_code" : 500, "detail" : "Token generation failed, login again"}

    return {
        "status": 200,
        "data": response.json(),
        "user": result
    }

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    
    if not user["exists"] or not verify_password(form_data.password, user["data"]["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response = requests.post(settings.JWT_API_URL + "/jwt/token", json={
        "username": form_data.username,
        "password": form_data.password
    })

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Token generation failed")

    return response.json()
