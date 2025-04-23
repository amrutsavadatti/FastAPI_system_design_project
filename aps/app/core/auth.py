import httpx
from fastapi import Request, HTTPException, status
from app.core.config import settings

async def validate_jwt(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    async with httpx.AsyncClient() as client:
        res = await client.post(settings.JWT_VALIDATE_URL, json={"access_token": token})
        if res.status_code != 200:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return res.json()
