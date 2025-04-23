from datetime import datetime
from app.db.fake_profiles import profiles_db

def save_user_profile(user_id: str, profile_data: dict):
    profiles_db[user_id] = {
        **profile_data,
        "user_id": user_id,
        "updated_at": datetime.utcnow()
    }
    return profiles_db[user_id]

def get_profile_by_user(user_id: str):
    return profiles_db.get(user_id)
