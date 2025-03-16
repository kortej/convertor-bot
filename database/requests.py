from database.db import async_session
from database.db import User
from sqlalchemy import select, update, delete


async def set_user(tg_id, user_name):
    async with async_session() as session:
        user_tg = await session.scalar(select(User).where(User.tg_id == tg_id))
        username = await session.scalar(select(User).where(User.user_name == user_name))

        if not user_tg:
            session.add(User(tg_id=tg_id))
            await session.commit()

        if not username:
            session.add(User(user_name=user_name))
            await session.commit()

    