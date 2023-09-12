import os

from contextvars import ContextVar, Token
from importlib import import_module
from typing import Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.expression import Update, Delete, Insert

from app.core.config import config

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engines = {
    "writer": create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
    "reader": create_async_engine(config.READER_DB_URL, pool_recycle=3600),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        else:
            return engines["reader"].sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
)
session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)
Base = declarative_base()


async def init_models():
    if config.ENV == 'prod':
        return

    async with engines['writer'].begin() as conn:
        # Drop and create all Base classes
        for _, _, files in os.walk('app/core/models'):
            for file in files:
                if not file.endswith('.py') or file.startswith('__'):
                    continue
                module_name = f'app.core.models.{file[:-3]}'
                module = import_module(module_name)
                for name in dir(module):
                    item = getattr(module, name)
                    if not hasattr(item, '__module__'):
                        continue
                    if not hasattr(item, 'metadata'):
                        continue
                    if not item.__module__.startswith(module_name):
                        continue

                    await conn.run_sync(item.metadata.drop_all)
                    await conn.run_sync(item.metadata.create_all)
