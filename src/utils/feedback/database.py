from uuid import UUID

from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import FeedBackAboutClients
from src.schemas import CreateFeedBackAboutClient


async def feedbacks_by_phone_number(
    session: AsyncSession, phone_number: str
) -> list[FeedBackAboutClients] | None:
    query = select(FeedBackAboutClients).where(
        FeedBackAboutClients.number_phone_of_client == phone_number
    )
    return await session.scalars(query)


async def add_feedback_about_client(
    session: AsyncSession, data: CreateFeedBackAboutClient, legal_entity_id: UUID
) -> bool:
    feedback = data.dict(exclude_unset=True)
    feedback.update({"legal_entity_id": legal_entity_id})
    session.add(FeedBackAboutClients(**feedback))
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True
