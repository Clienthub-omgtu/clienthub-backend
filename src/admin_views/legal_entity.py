from typing import Any, Dict

from starlette_admin.contrib.sqla import ModelView

from starlette.exceptions import HTTPException
from starlette import status
from starlette.requests import Request

from sqlalchemy.exc import IntegrityError

from src.db.models import LegalEntity


class LegalEntityView(ModelView):
    label = "Legal entities"
    model = LegalEntity
    fields = ["email", "name", "ogrn", "ogrnip", "inn", "subscription_expiration_date"]

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        try:
            return await super().create(request=request, data=data)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=exc.orig
            )
