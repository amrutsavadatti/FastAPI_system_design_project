from fastapi import APIRouter

router = APIRouter()

@router.get("/check", tags=["Health"])
def health_check():
    return {"status": "ok"}