from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.profile import UserProfile
from app.services.profile import *
from app.core.mongo import get_collection
import requests
from app.core.config import settings

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.get("/profiles/{user_id}")
async def get_profile_by_id(user_id: str, token: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    access_token = token.credentials
    response = requests.post(settings.JWT_API_URL + "/jwt/validate", json={"access_token": access_token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profile = await get_profile_by_user_id(user_id)
    profile["_id"] = str(profile["_id"])  # Convert ObjectId to string
    return {"profile": profile}


@router.get("/profiles")
async def list_profiles(limit: int = 10, token: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    access_token = token.credentials
    response = requests.post(settings.JWT_API_URL + "/jwt/validate", json={"access_token": access_token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profiles_collection = get_collection("profiles")
    cursor = profiles_collection.find().limit(limit)
    profiles = await cursor.to_list(length=limit)
    for p in profiles:
        p["_id"] = str(p["_id"])  # Make ObjectId JSON serializable
    return {"profiles": profiles}


@router.put("/profiles")
async def update_profile(update_data:UserProfile, token: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    access_token = token.credentials
    response = requests.post(settings.JWT_API_URL + "/jwt/validate", json={"access_token": access_token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    result = await update_profile_by_user_id(update_data)
    if result["status"] != 200:
        raise HTTPException(status_code=500, detail="Failed to update profile")
    else:
        return {"status": 200}