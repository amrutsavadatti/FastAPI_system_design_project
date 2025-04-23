from fastapi import FastAPI
from app.routes import health, token

app = FastAPI(title="JWT Auth API", debug=True)

app.include_router(token.router, prefix="/jwt", tags=["Token"])
app.include_router(health.router, prefix="/health", tags=["Health"])
