from enum import Enum

class FitType(str, Enum):
    SLIM = "slim"
    REGULAR = "regular"
    OVERSIZED = "oversized"

class HeightUnit(str, Enum):
    CM = "centimeter"
    M = "meters"
    I = "inch"

class WeightUnit(str, Enum):
    KG = "kilograms"
    LBS = "pounds"

class SexEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

# # Usage
# fit = FitType.SLIM
# print(fit.value)