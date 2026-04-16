from typing import Optional, Union
import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator
from cinescope.constants import Roles, Location


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="passwordRepeat должен полностью совпадать с полем password")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:

        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


    class Config:
        json_encoders = {
            Roles: lambda v: v.value
        }

class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

class TestMovie(BaseModel):
    name: str
    imageUrl: str
    price: int = Field(gt=0)
    description: str = Field(..., min_length=1, max_length=250)
    location: str
    published: bool
    genreId: int

class TestMovieResponse(BaseModel):
    id: int
    name: str
    price: int = Field(gt=0)
    description: str = Field(..., min_length=1, max_length=250)
    imageUrl: str
    location: str
    published: bool
    rating: int
    genreId: int
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")
    reviews: Optional[list] = None
    genre: dict[str,str]

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value


class TestMovieNegativeResponse(BaseModel):
    message: Union[str, list]
    error: str
    statusCode: int
