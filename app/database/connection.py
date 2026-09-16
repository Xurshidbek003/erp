from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession
from app.utils.config import settings

DB_USERNAME = settings.DB_USERNAME
DB_PASSWORD = settings.DB_PASSWORD
DB_NAME = settings.DB_NAME


engine = create_async_engine(f"mysql+aiomysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}")


SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as db:
        yield db