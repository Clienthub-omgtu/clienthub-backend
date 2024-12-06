from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.connection import get_session
from src.db.models import User
from src.schemas import InviteSuccess, InviteEmployee, LegalEntityRead, UserRole

from src.utils.legal_entity import invite_employee, send_invite_mail, get_legal_entity

from src.utils.user import get_current_user


api_router = APIRouter(
    prefix="/legal_entity",
    tags=["Legal entity"],
)


@api_router.post(
    "/add_user_to_organization",
    status_code=status.HTTP_200_OK,
    response_model=InviteSuccess,
    responses={status.HTTP_403_FORBIDDEN: {"description": "Access denied"}},
)
async def invite_employee_to_org(
    _: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    potential_employee: InviteEmployee = Body(...),
):
    if current_user.role.value != UserRole.ADMIN_OF_ORGANIZATION.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    is_success, message, email = await invite_employee(
        session=session, potential_employee=potential_employee
    )
    if is_success:
        await send_invite_mail(email)
        return {"message": message}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


@api_router.post(
    "/get_legal_entity_inf_by_id",
    status_code=status.HTTP_200_OK,
    response_model=LegalEntityRead,
    responses={status.HTTP_200_OK: {"description": "success"}},
)
async def get_legal_entity_inf_by_id(
    _: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_legal_entity(
        session=session, legal_entity_id=str(current_user.legal_entity_id)
    )
