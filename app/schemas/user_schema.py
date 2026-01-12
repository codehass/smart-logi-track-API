from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from typing import List


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class TrajectFeaturesRequest(BaseModel):
    trip_distance: float
    fare_amount: float
    tip_amount: float
    tolls_amount: float
    total_amount: float
    Airport_fee: float
    RatecodeID: int
    pickuphour: int
    dayof_week: int
