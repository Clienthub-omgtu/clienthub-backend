from uuid import UUID

from fastapi_mail import MessageType, MessageSchema, FastMail
from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Payment, Configuration
from yookassa.domain.response import PaymentResponse

from src.config import get_settings
from src.db.models import User
from src.schemas import PaymentCreate, PaymentConfirmed
from .database import add_payment, get_payment_by_id, approve_payment

Configuration.account_id = get_settings().YOOKASSA_ACCOUNT_ID
Configuration.secret_key = get_settings().YOOKASSA_SECRET_KEY


async def send_invite_mail(email: str) -> None:
    settings = get_settings()

    text = "Вы добавлены в организацию"

    message = MessageSchema(
        subject="ClientHub Invite",
        recipients=[email],
        body=text,
        subtype=MessageType.html,
    )

    sender = FastMail(settings.mail_connect_config)
    await sender.send_message(message)


async def create_payment_yookassa(
    session: AsyncSession, legal_entity_id: UUID
) -> PaymentResponse | None:
    new_payment = PaymentCreate(**{"legal_entity_id": legal_entity_id})
    settings = get_settings()
    payment = Payment.create(
        {
            "amount": {
                "value": settings.AMOUNT,
                "currency": "RUB",
            },
            "capture": True,
            "confirmation": {"type": "redirect", "return_url": settings.REDIRECT_URL},
        }
    )
    new_payment.payment_id = payment.id
    is_success, message = await add_payment(
        session=session, potential_payment=new_payment
    )
    if is_success:
        return payment
    return None


async def confirm_payment(
    session: AsyncSession, payment_id: UUID, user: User
) -> PaymentConfirmed:
    payment = await get_payment_by_id(session=session, payment_id=payment_id)
    if not payment:
        return PaymentConfirmed(
            **{
                "status_code": 404,
                "message": "Payment not found",
                "is_confirmed": False,
            }
        )
    curr_status_of_payment = Payment.find_one(str(payment_id)).status
    if not payment.is_confirmed and curr_status_of_payment == "succeeded":
        is_success = await approve_payment(
            session=session, payment_id=payment_id, legal_entity_id=user.legal_entity_id
        )
        if is_success:
            return PaymentConfirmed(
                **{"status_code": 200, "message": "Successfully", "is_confirmed": True}
            )
    return PaymentConfirmed(
        **{"status_code": 400, "message": "Some error", "is_confirmed": False}
    )
