from fastapi import APIRouter

router = APIRouter()

@router.get("/check", tags=["health"])
def health_check():
    return {"status": "healthy"}
