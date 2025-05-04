from datetime import datetime
from fastapi import HTTPException
import os
from app.core.mongo import get_collection
from app.models.profile import UserProfile



profiles_collection = get_collection("profiles")

async def create_profile(user_id:str):
    existing = await profiles_collection.find_one({"user_id": user_id})
    if existing:
        return {"success": False, "message": "Profile already exists"}

    profile = UserProfile(user_id=str(user_id))
    result = await profiles_collection.insert_one(profile.model_dump())
    if result.inserted_id:
        return {"success": True}
    else:
        raise HTTPException(status_code=500, detail="Failed to create profile")
    
async def get_profile_by_user_id(user_id:str):
    profile = await profiles_collection.find_one({"user_id": user_id})
    if profile:
        return profile
    else:
        raise HTTPException(status_code=500, detail="User profile does not exists")
    
async def update_profile_by_user_id(update_data:UserProfile):
    result = await profiles_collection.update_one(
        {"user_id": update_data.user_id},
        {"$set": update_data.model_dump()},
        upsert=False  # or True if you want to insert when missing
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"status": 200, "updated_count": result.modified_count}