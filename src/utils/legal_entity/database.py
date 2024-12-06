import datetime
from uuid import UUID

from sqlalchemy import exc, select, update, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import LegalEntity, User, Payments
from src.schemas import LegalEntityCreate, InviteEmployee, PaymentCreate


async def get_legal_entity(
    session: AsyncSession, legal_entity_id: str
) -> LegalEntity | None:
    query = select(LegalEntity).where(LegalEntity.id == legal_entity_id)
    return await session.scalar(query)


async def register_legal_entity(
    session: AsyncSession, potential_legal_entity: LegalEntityCreate
) -> tuple[bool, str, LegalEntity | None]:
    legal_entity = LegalEntity(**potential_legal_entity.dict(exclude_unset=True))
    session.add(legal_entity)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False, "Organization already exists", None
    return True, "Successful registration!", legal_entity


async def invite_employee(
    session: AsyncSession, potential_employee: InviteEmployee
) -> tuple[bool, str, str | None]:
    employee = User(**potential_employee.dict(exclude_unset=True))
    session.add(employee)
    try:
        await session.commit()
    except exc.IntegrityError:
        return (
            False,
            "User with this email already exists or defunct organization.",
            None,
        )
    return True, "Successful registration!", employee.email


async def add_payment(
    session: AsyncSession, potential_payment: PaymentCreate
) -> tuple[bool, str]:
    payment = Payments(**potential_payment.dict(exclude_unset=True))
    session.add(payment)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False, "some_error"
    return True, "successfully"


async def get_not_confirmed_payments(
    session: AsyncSession, legal_entity_id: UUID
) -> ScalarResult[Payments]:
    query = select(Payments).where(
        (Payments.legal_entity_id == legal_entity_id) & (Payments.is_confirmed == False)
    )
    return await session.scalars(query)


async def approve_payment(
    session: AsyncSession, payment_id: UUID, legal_entity_id: UUID
) -> bool:
    legal_entity = await get_legal_entity(
        session=session, legal_entity_id=str(legal_entity_id)
    )
    update_payment = (
        update(Payments)
        .where(Payments.payment_id == payment_id)
        .values({"is_confirmed": True})
    )
    update_subscription = (
        update(LegalEntity)
        .where(LegalEntity.id == legal_entity_id)
        .values(
            {
                "subscription_expiration_date": (
                    legal_entity.subscription_expiration_date
                    if legal_entity.subscription_expiration_date
                    else datetime.datetime.now()
                )
                + datetime.timedelta(days=30)
            }
        )
    )
    try:
        await session.execute(update_payment)
        await session.execute(update_subscription)
        await session.commit()
    except exc.IntegrityError:
        await session.rollback()
        return False
    return True


async def get_payment_by_id(session: AsyncSession, payment_id: UUID):
    query = select(Payments).where(Payments.payment_id == payment_id)
    return await session.scalar(query)
