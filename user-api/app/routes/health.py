from fastapi import APIRouter

router = APIRouter()

@router.get("/check", tags=["health"])
def health_check():
    print("Health check")
    return {"status": "ok1"}
