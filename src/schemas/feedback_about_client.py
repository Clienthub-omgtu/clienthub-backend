from typing import Annotated, Optional

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class CreateFeedBackAboutClient(BaseModel):
    email_of_client: Annotated[Optional[EmailStr], Field(max_length=255)]
    first_name_of_client: Annotated[Optional[str], Field(max_length=255)]
    middle_name_of_client: Annotated[Optional[str], Field(max_length=255)]
    last_name_of_client: Annotated[Optional[str], Field(max_length=255)]
    number_phone_of_client: Annotated[Optional[str], Field(max_length=100)]
    telegram_nickname_of_client: Annotated[Optional[str], Field(max_length=255)]
    description: Annotated[str, Field(max_length=500)]
    grade: Annotated[int, Field()]

    model_config = ConfigDict(from_attributes=True)

    @field_validator("grade")
    def validate_grade(cls, grade: int):
        if not 1 <= grade <= 10:
            raise ValueError("Field 'grade' must be int between 1 and 10")
        return grade


class FeedBacksByPhoneNumber(BaseModel):
    phone_number: Annotated[str, Field()]


class ReadFeedBackAboutClient(BaseModel):
    description: Annotated[str, Field(max_length=500)]
    grade: Annotated[int, Field()]


class AddFeedbackSuccess(BaseModel):
    message: str
