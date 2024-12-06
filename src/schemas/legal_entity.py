from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, field_validator

from .user import UserRole


class LegalEntityBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=255)]
    email: Annotated[EmailStr, Field(max_length=255)]
    ogrn: Annotated[str, Field(min_length=13, max_length=13)]
    ogrnip: Annotated[str, Field(min_length=15, max_length=15)]
    inn: Annotated[str, Field(min_length=10, max_length=10)]


class LegalEntityRead(LegalEntityBase):
    pass


class LegalEntityCreate(LegalEntityBase):
    pass


class InviteEmployee(BaseModel):
    email: Annotated[EmailStr, Field(max_length=255)]
    legal_entity_id: Annotated[UUID, Field()]
    role: Annotated[str, Field(default="employee")]

    @field_validator("role")
    def validate_role(cls, value: Optional[str]) -> str | ValueError:
        if value is None:
            raise ValueError("User must have role")
        if value not in UserRole.__members__.values():
            raise ValueError(
                f"Invalid role of user: {value}. Must be one of {list(UserRole)}"
            )
        return value


class InviteSuccess(BaseModel):
    message: str
