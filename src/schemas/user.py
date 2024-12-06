import enum
from typing import Annotated

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from src.config import get_settings


class UserRole(str, enum.Enum):
    EMPLOYEE = "employee"
    ADMIN_OF_ORGANIZATION = "org_admin"


class UserBase(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=255)]
    middle_name: Annotated[str, Field(min_length=2, max_length=255)]
    last_name: Annotated[str, Field(min_length=2, max_length=255)]

    model_config = ConfigDict(from_attributes=True)


class UserRegistration(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=255)]
    email: Annotated[EmailStr, Field(max_length=255)]

    @field_validator("password")
    def validate_password(cls, password: str, is_registered: bool) -> str | ValueError:
        if password is None and not is_registered:
            raise ValueError("User must have password")
        if (
            not any(c.isupper() for c in password)
            or not any(c.islower() for c in password)
            or not any(c.isdigit() for c in password)
        ):
            raise ValueError(
                "The password must contain at least one uppercase and"
                " at least one lowercase letter and numbers."
            )
        settings = get_settings()
        password = settings.PWD_CONTEXT.hash(password)
        return password


class UserRead(UserBase):
    email: Annotated[EmailStr, Field(max_length=255)]
    role: Annotated[str, Field()]


class RegistrationSuccess(BaseModel):
    message: str


class UserUpdatedSuccess(BaseModel):
    message: str


class UserUpdate(UserBase):
    email: Annotated[EmailStr, Field(max_length=255)]
