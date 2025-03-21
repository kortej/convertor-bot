from database.db import async_session
from database.db import User
from sqlalchemy import select


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.username = username
        else:
            user = User(tg_id=tg_id, username=username)
            session.add(user)
        
        await session.commit()


async def get_user(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()


async def is_user_in_db(tg_id: int) -> bool:
    async with async_session() as session: 
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalars().first()
        return user is not None


async def counter(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.count_converts += 1
        
            await session.commit()

        
async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        
        users = result.scalars().all()
        return users
        