import uuid

from sqlalchemy import UUID, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

sqlite_database = 'sqlite+aiosqlite:///db/bot.db'

engine = create_async_engine(sqlite_database, echo=False)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        unique=True,
    )


class Zuzubliks(Base):
    __tablename__ = 'zuzubliks'
    title: Mapped[str] = mapped_column(String(50), unique=False)
    url: Mapped[str] = mapped_column(String(50), unique=False)
    xpath: Mapped[str] = mapped_column(String(50), unique=False)


class Repozitory:
    @classmethod
    async def get_or_create(self, model, **kwargs):
        async with new_session() as session:
            rez = await session.execute(select(model).filter_by(**kwargs))
            instance = rez.scalars().first()
            if instance:
                return instance
            else:
                instance = model(**kwargs)
                session.add(instance)
                await session.flush()
                await session.commit()
                return instance

    @classmethod
    async def create_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
