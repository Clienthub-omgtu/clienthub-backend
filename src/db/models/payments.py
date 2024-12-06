from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

if TYPE_CHECKING:
    from src.db.models import LegalEntity


class Payments(Base):
    """
    Represents a user in the application.

    This class maps to the 'users' table in the database and contains
    attributes related to user information, roles, and relationships with
    other entities in the application.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The user's email address, which must be unique.
        firstname (str): The user's first name.
        lastname (str): The user's last name.
        middlename (Optional[str]): The user's middle name (if applicable).
        role (UserRole): The role of the user, defined as an enumeration.
        password (str): The user's password (hashed).
        legal_entity_id (Optional[int]): The ID of the legal entity the user belongs to.

    Relationships:
        legal_entity (Optional[LegalEntity]): The legal entity associated with the user.
    """

    __tablename__ = "payment"

    repr_cols = ("id", "is_confirmed")

    is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    payment_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        doc="Unique payment id (type UUID))",
    )

    legal_entity_id: Mapped[UUID] = mapped_column(
        ForeignKey("legal_entity.id", ondelete="SET NULL"), nullable=False
    )

    legal_entity: Mapped[Optional["LegalEntity"]] = relationship(
        "LegalEntity",
        back_populates="payments",
        lazy="selectin",
    )
