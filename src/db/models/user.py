import enum
from uuid import UUID
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from starlette.requests import Request
from starlette.responses import Response

from .base import Base

if TYPE_CHECKING:
    from src.db.models import LegalEntity


class UserRole(enum.Enum):
    """
    Enumeration of user roles within the application.

    Attributes:
        EMPLOYEE: Base user.
        ADMIN_OF_ORGANIZATION: The admin of organization.
    """

    EMPLOYEE = "employee"
    ADMIN_OF_ORGANIZATION = "org_admin"


class User(Base):
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

    __tablename__ = "users"

    repr_cols = ("id", "email", "firstname", "lastname")

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=True)

    last_name: Mapped[str] = mapped_column(String(100), nullable=True)

    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(
            UserRole,
            native_enum=False,
            name="user_role_enum",
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=False,
    )

    password: Mapped[str] = mapped_column(String(255), nullable=True)

    legal_entity_id: Mapped[UUID] = mapped_column(
        ForeignKey("legal_entity.id", ondelete="SET NULL"), nullable=False
    )

    legal_entity: Mapped[Optional["LegalEntity"]] = relationship(
        "LegalEntity", back_populates="users", lazy="selectin"
    )

    is_registered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
