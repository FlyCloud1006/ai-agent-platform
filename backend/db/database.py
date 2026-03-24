from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = None
async_session_maker = None

async def init_db():
    global engine, async_session_maker
    from config import config
    
    engine = create_async_engine(
        config.DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20,
    )
    
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
