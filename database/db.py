from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///format_bot.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Модель користувача
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    conversions = relationship("Conversion", back_populates="user")


# Модель для лічильника конвертацій
class Conversion(Base):
    __tablename__ = 'conversions'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    count = Column(Integer, default=0)
    user = relationship("User", back_populates="conversions")


# create data table 
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)