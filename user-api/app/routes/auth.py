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
def signup(user: UserSignup,  db: Session = Depends(get_db)):

    result = create_user_account(db, user.email, user.password)
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
        "data": response.json()
    }

    #
    # get_user_by_email(db, str(user.email))
    # result = db.execute(
    #     text("SELECT * FROM users WHERE email = :email"),
    #     {"email": "john@example.com"}
    # )
    #
    # rows = result.fetchall()
    # for row in rows:
    #     print(row)
    #
    # if result:
    #     print(result)
    #     return {"message": "User already exists"}
    #
    # print(settings.JWT_API_URL + "/token")
    # response = requests.post(settings.JWT_API_URL + "/token", json={
    #     "username": user.username,
    #     "password": user.password
    # })
    #
    #
    # if response.status_code != 200:
    #     raise HTTPException(status_code=500, detail="Token generation failed")
    #
    # return response.json()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response = requests.post(settings.JWT_API_URL + "/token", data={
        "username": form_data.username,
        "password": form_data.password
    })


    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Token generation failed")

    return response.json()
