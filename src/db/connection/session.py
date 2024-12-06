from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Engine

from src.config import get_settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    def get_sync_session_maker(self) -> sessionmaker:
        return sessionmaker(self.sync_engine, expire_on_commit=False)

    def refresh(self) -> None:
        self.engine = create_async_engine(
            get_settings().database_url_async, echo=True, future=True
        )
        self.sync_engine = create_engine(
            get_settings().database_url_sync, echo=True, future=True
        )


async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


def get_sync_session() -> Session:
    session_maker = SessionManager().get_sync_session_maker()
    with session_maker() as session:
        return session


def get_sync_engine() -> Engine:
    engine = create_engine(get_settings().database_url_sync)
    return engine
