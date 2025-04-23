from fastapi import APIRouter, HTTPException
from app.models.token import TokenRequest, RefreshTokenRequest, TokenValidateRequest
from app.core.jwt_handler import create_access_token, create_refresh_token, decode_token

router = APIRouter()

@router.post("/token")
def generate_token(payload: TokenRequest):
    data = {"sub": payload.username}
    try:
        return {
            "access_token": create_access_token(data),
            "refresh_token": create_refresh_token(data),
            "token_type": "bearer"
        }
    except Exception as e:
        return HTTPException(status_code=401, detail=e)

@router.post("/refresh")
def refresh_token(req: RefreshTokenRequest):
    decoded = decode_token(req.refresh_token)
    if not decoded:
        return HTTPException(status_code=401, detail="Invalid refresh token")
    try:
        return {"access_token": create_access_token({"sub": decoded["sub"]})}
    except Exception as e:
        return HTTPException(status_code=401, detail=e)

@router.post("/validate")
def validate_token(req: TokenValidateRequest):
    try:
        decoded = decode_token(req.access_token)
        if not decoded:
            return HTTPException(status_code=401, detail="Invalid token")
        return {"status_code": 200,"user": decoded["sub"], "exp": decoded["exp"]}
    except Exception as e:
        return HTTPException(status_code=401, detail=e)
