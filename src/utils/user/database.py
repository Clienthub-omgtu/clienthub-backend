from typing import List
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc

from src.db.models import User
from src.schemas import UserBase, UserRegistration, UserUpdate


async def get_user(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    return await session.scalar(query)


async def get_registered_user(session: AsyncSession, email: str) -> User | None:
    query = select(User).where((User.email == email) & (User.is_registered == True))
    return await session.scalar(query)


async def register_user(
    session: AsyncSession, potential_user: UserRegistration
) -> tuple[bool, str, str | None]:
    user = await get_user(session=session, email=potential_user.email)
    if user and not user.is_registered:
        potential_user = potential_user.dict(exclude_unset=True)
        potential_user.update({"is_registered": True})

        update_user_query = (
            update(User).where(User.id == user.id).values(**potential_user)
        )

        await session.execute(update_user_query)
        await session.commit()

        return True, "Successfull registration", user.email

    return False, "User not exist or already registered", None


async def get_not_registered_users(
    session: AsyncSession, legal_entity_id: UUID
) -> List[UserBase]:
    query = select(User).where(
        (User.is_approved is None) & (User.legal_entity == legal_entity_id)
    )
    return await session.scalars(query)


async def update_user(session: AsyncSession, data: UserUpdate, curr_user: User) -> bool:
    query_for_update = (
        update(User)
        .where(User.email == curr_user.email)
        .values(**data.dict(exclude_unset=True))
    )
    try:
        await session.execute(query_for_update)
        await session.commit()
    except exc.IntegrityError:
        return False
    return True


async def delete_user(session: AsyncSession, user: User) -> None:
    query = delete(User).where(User.email == user.email)
    await session.execute(query)
    await session.commit()
