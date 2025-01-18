from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    tg_user_id: Optional[int] = None
    password: str = Field(..., min_length=3, max_length=60)
    phone: PhoneNumber = None

class UserInfoResponse(BaseModel):
    id: int
    tg_user_id: Optional[int]
    username: str
    phone: Optional[PhoneNumber]
    role_id: int

class UserTokenResponse(BaseModel):
    token: str
    success: bool

class UserAuthRequest(BaseModel):
    username: str | int
    password: str
