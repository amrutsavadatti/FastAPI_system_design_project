from pydantic import BaseModel
from typing import List, Optional
from app.utils.enums import *

class UserProfile(BaseModel):
    sex: str
    height: int
    h_unit: HeightUnit
    weight: int
    w_unit: WeightUnit
    preferred_fit: FitType
    favorite_color: List[str]
    preferred_styles: List[str]
    body_shape: Optional[str] = None
    measurements: Optional[dict] = None
