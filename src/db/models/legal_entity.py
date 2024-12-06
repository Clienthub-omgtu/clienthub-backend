from typing import TYPE_CHECKING, List
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from src.db.models import User, Payments, FeedBackAboutClients


class LegalEntity(Base):
    __tablename__ = "legal_entity"

    repr_cols = ("id", "name")

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    ogrn: Mapped[str] = mapped_column(
        String(13), unique=True, index=True, nullable=False
    )

    ogrnip: Mapped[str] = mapped_column(
        String(15), unique=True, index=True, nullable=True
    )

    inn: Mapped[str] = mapped_column(
        String(10), unique=True, index=True, nullable=False
    )

    subscription_expiration_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False), nullable=True
    )

    users: Mapped[List["User"]] = relationship("User", back_populates="legal_entity")

    payments: Mapped[List["Payments"]] = relationship(
        "Payments", back_populates="legal_entity"
    )

    feedbacks_about_client: Mapped[List["Payments"]] = relationship(
        "FeedBackAboutClients", back_populates="legal_entity"
    )
