from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    legal_entity_id: Annotated[UUID, Field()]
    payment_id: UUID = None


class PaymentConfirmed(BaseModel):
    message: str
    is_confirmed: bool
    status_code: int


class PaymentConfirm(BaseModel):
    payment_id: UUID
