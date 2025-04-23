from fastapi import APIRouter, Depends, Request
from app.core.auth import validate_jwt
from app.core.config import settings
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

from app.services.some_brand import get_products

router = APIRouter()
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    token = credentials.credentials
    if not token or token == "invalid":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return {"user_id": "123", "role": "user"}

@router.get("/feed")
async def get_feed(user=Depends(validate_jwt)):
    print(user)
    if user["status_code"] == 200:
        res = await get_products()
        return res
    else:
        return user
