from fastapi import FastAPI
from app.routes import proxy, health

app = FastAPI(title="Api Proxy Service")

app.include_router(health.router, prefix="/aps")
app.include_router(proxy.router, prefix="/aps")