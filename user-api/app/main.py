from fastapi import FastAPI
from app.routes import auth, profile, health

app = FastAPI(title="User_API", debug=True)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])