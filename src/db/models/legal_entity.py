from typing import TYPE_CHECKING, List
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from src.db.models import User, Payments, FeedBackAboutClients


class LegalEntity(Base):
    """
    Represents a legal_entity in the application.

    This class maps to the 'legal_entity' table in the database and contains
    attributes related to user information and relationships with
    other entities in the application.

    Attributes:
        id (uuid): The unique identifier for the legal entity.
        email (str): The legal_entity email address, which must be unique.
        name (str): The legal entity name.
        ogrn (str): The ogrn legal entity.
        ogrnip (str): The legal entity.
        inn (str): The inn of the legal_entity.
        subscription_expiration_date(DateTime): The subscription_expiration_date legal_entity.

    Relationships:
        users (User): The legal entity associated with the user.
        payments (Payments): The legal entity associated with the payments.
        feedbacks_about_client (FeedBackAboutClients): The legal entity associated with feedbacks.
    """

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

    feedbacks_about_client: Mapped[List["FeedBackAboutClients"]] = relationship(
        "FeedBackAboutClients", back_populates="legal_entity"
    )
