from database.db import async_session
from database.db import User
from sqlalchemy import select, update, delete


async def set_user(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id, name=name)
            session.add(new_user)
            await session.commit()


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            return {'name': user.name}
        else:
            return 'db have no your profile'
    