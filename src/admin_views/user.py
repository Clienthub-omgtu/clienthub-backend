from typing import Any, Dict

from starlette_admin.contrib.sqla import ModelView

from starlette.exceptions import HTTPException
from starlette import status
from starlette.requests import Request

from sqlalchemy.exc import IntegrityError

from src.db.models import User


class UserView(ModelView):
    label = "Users"
    model = User
    fields = [
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "role",
        "legal_entity_id",
        "legal_entity",
        "is_registered",
    ]
    form_include_pk = True

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
