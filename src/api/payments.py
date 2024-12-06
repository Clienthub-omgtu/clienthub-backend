from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.connection import get_session
from src.db.models import User
from src.schemas import UserRole, PaymentConfirm, PaymentConfirmed

from src.utils.user import get_current_user
from src.utils.legal_entity import create_payment_yookassa, confirm_payment


api_router = APIRouter(
    prefix="/payments",
    tags=["Payment"],
)


@api_router.post("/create_payment", status_code=status.HTTP_200_OK)
async def create_payment(
    _: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value != UserRole.ADMIN_OF_ORGANIZATION.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    data = await create_payment_yookassa(
        session=session, legal_entity_id=current_user.legal_entity_id
    )
    if data:
        return data
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@api_router.post(
    "/confirm_payment",
    status_code=status.HTTP_200_OK,
    response_model=PaymentConfirmed,
)
async def confirmation_payment(
    _: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    payment: PaymentConfirm = Body(...),
):
    payment_confirmed = await confirm_payment(
        session=session, payment_id=payment.payment_id, user=current_user
    )
    if payment_confirmed.is_confirmed and payment_confirmed.status_code == 200:
        return payment_confirmed
    if not payment_confirmed.is_confirmed:
        raise HTTPException(status_code=400, detail=payment_confirmed.message)
