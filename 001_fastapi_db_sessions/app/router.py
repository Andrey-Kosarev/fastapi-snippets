from fastapi import APIRouter, Depends
from connection import get_async_session_manager, AsyncSessionManager, get_sync_session_manager, \
    SyncSessionManager
from sqlalchemy import text
import asyncio

root_router = APIRouter()


async def execute_query(session_manager: AsyncSessionManager, query: str):
    async with session_manager.get_session() as session:
        query = await session.execute(text(query))
    return query.scalar()


def sync_execute_query(session, query: str):
    query = session.execute(text(query))
    return query.scalar()


@root_router.get("/")
async def get_async(session_manager: AsyncSessionManager = Depends(get_async_session_manager)):
    tasks = [
        execute_query(session_manager, "SELECT version()"),
        execute_query(session_manager, "SELECT now()")
    ]

    query_results = await asyncio.gather(*tasks)

    return {
        "data": query_results,
    }


@root_router.get("/sync")
def get_sync(session_manager: SyncSessionManager = Depends(get_sync_session_manager)):

    with session_manager.get_session() as session:
        query_results = [
            sync_execute_query(session, "SELECT pg_sleep(0.1)"),
            sync_execute_query(session, "SELECT pg_sleep(0.1)")
        ]

    return {
        "data": query_results,
    }
