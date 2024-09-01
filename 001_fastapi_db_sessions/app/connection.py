from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from asyncio import current_task


DEBUG = False
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'database'  #  'localhost:5432'
DB_NAME = 'sample_db'
DB_STRING = f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
POOL_SIZE=10

engine_async = create_async_engine(f"postgresql+asyncpg://{DB_STRING}")
engine_sync = create_engine(f"postgresql://{DB_STRING}")

session_local = sessionmaker(engine_sync)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SyncSessionManager(metaclass=Singleton):
    def __init__(self):
        self.session_scope = scoped_session(sessionmaker(engine_sync))

    def get_session(self):
        return self.session_scope()

    def clear_sessions(self):
        self.session_scope.remove()

class AsyncSessionManager(metaclass=Singleton):
    def __init__(self):
        self.session_scope = async_scoped_session( async_sessionmaker(engine_async), scopefunc=lambda: id(current_task()) )

    def get_session(self):
        return self.session_scope()

    async def clear_sessions(self):
        await self.session_scope.remove()



async def get_async_session_manager():
    session_manager = AsyncSessionManager()
    try:
        yield session_manager
    finally:
        await session_manager.clear_sessions()


def get_sync_session_manager():
    session_manager = SyncSessionManager()
    try:
        yield session_manager
    finally:
        session_manager.clear_sessions()