from typing import Any, Dict

from starlette_admin.contrib.sqla import ModelView

from starlette.exceptions import HTTPException
from starlette import status
from starlette.requests import Request

from sqlalchemy.exc import IntegrityError

from src.db.models import Payments


class PaymentView(ModelView):
    label = "Payments"
    model = Payments
    fields = ["is_confirmed", "payment_id", "legal_entity_id", "legal_entity"]

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        if not data["legal_entity"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="legal_entity field is required",
            )

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        try:
            return await super().create(request=request, data=data)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=exc.orig
            )