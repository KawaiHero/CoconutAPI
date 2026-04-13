from typing import Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from venv import logger

from cinescope.constants import Roles
from cinescope.utils.data_generator import DataGenerator

class User(BaseModel):
    email: str = Field(..., min_length=3, max_length=50, description="email")
    fullName: str
    password: str
    roles: list[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("email")
    def validate_email(cls, value:str) -> str:
        if "@" not in value:
            raise ValueError("email должен содержать @")
        return value

    @field_validator("password")
    def password_length(cls, value:str) -> str:
        if len(value) < 8:
            raise ValueError("password должен содержать как минимум 8 знаков")
        return value


def test_pyd_user(test_user):
    user = test_user.copy()
    p_user = User(**user)
    json_data = p_user.model_dump_json(exclude_unset=True)
    print(json_data)

def test_pyd_cr_user(creation_user_data):
    user = creation_user_data.copy()
    p_user = User(**user)
    json_data = p_user.model_dump_json()
    print(json_data)