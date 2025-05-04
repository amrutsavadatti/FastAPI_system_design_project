from pydantic import BaseModel
from typing import List, Optional
from app.utils.enums import *

class UserProfile(BaseModel):
    user_id: str
    sex: Optional[str] = None
    height: Optional[int] = None
    h_unit: Optional[HeightUnit] = None
    waist: Optional[int] = None
    w_unit: Optional[WaistUnit] = None
    preferred_fit: Optional[FitType] = None
    favorite_color: Optional[List[str]] = None
    preferred_styles: Optional[List[str]] = None
    body_shape: Optional[str] = None
    measurements: Optional[dict] = None
