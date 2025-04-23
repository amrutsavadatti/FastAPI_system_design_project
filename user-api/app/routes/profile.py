from fastapi import APIRouter, HTTPException
from app.models.profile import UserProfile
from app.services.profile import save_user_profile, get_profile_by_user
from app.services.user import users_db

router = APIRouter()

@router.post("/{user_id}")
def create_or_update_profile(user_id: str, profile: UserProfile):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    saved = save_user_profile(user_id, profile.model_dump())
    return {"message": "Profile saved", "profile": saved}

@router.get("/{user_id}")
def get_profile(user_id: str):
    profile = get_profile_by_user(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
