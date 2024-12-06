import uuid

from typing import Optional
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class FeedBackAboutClients(Base):
    __tablename__ = "feedback_about_client"

    repr_cols = ("id", "name")

    email_of_client: Mapped[str] = mapped_column(String(255), index=True, nullable=True)

    first_name_of_client: Mapped[str] = mapped_column(String(100), nullable=True)

    last_name_of_client: Mapped[str] = mapped_column(String(100), nullable=True)

    middle_name_of_client: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    number_phone_of_client: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )

    telegram_nickname_of_client: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )

    legal_entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("legal_entity.id", ondelete="SET NULL"), nullable=False
    )

    legal_entity: Mapped[Optional["LegalEntity"]] = relationship(
        "LegalEntity",
        back_populates="feedbacks_about_client",
        lazy="selectin",
    )

    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    grade: Mapped[int] = mapped_column(Integer, nullable=False)
