from typing import Any, Dict

from starlette_admin.contrib.sqla import ModelView

from starlette.exceptions import HTTPException
from starlette import status
from starlette.requests import Request

from src.db.models import FeedBackAboutClients


class FeedBackAboutClientsView(ModelView):
    label = "Feedbacks about client"
    model = FeedBackAboutClients
    fields = [
        "email_of_client",
        "first_name_of_client",
        "last_name_of_client",
        "middle_name_of_client",
        "number_phone_of_client",
        "telegram_nickname_of_client",
        "legal_entity_id",
        "legal_entity",
        "description",
        "grade",
    ]

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        if not data["legal_entity"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="legal_entity field is required",
            )
        if data["grade"] and not 0 <= data["grade"] <= 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="value of grade must be between 1 and 10",
            )
