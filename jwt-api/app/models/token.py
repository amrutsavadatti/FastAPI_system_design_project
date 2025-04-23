from pydantic import BaseModel

class TokenRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenValidateRequest(BaseModel):
    access_token: str
