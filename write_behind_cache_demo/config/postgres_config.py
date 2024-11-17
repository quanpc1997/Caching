from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .general_config import config

Base = declarative_base()

engine = create_async_engine(
    config.sqlalchemy_url,
    pool_size=config.pool_size,  # Số kết nối tối đa trong pool
    max_overflow=config.max_overflow,  # Số kết nối bổ sung khi pool đầy
    pool_timeout=config.pool_timeout,  # Thời gian chờ tối đa khi pool đầy trước khi raise lỗi
    pool_recycle=config.pool_recycle,  # Tái chế kết nối sau 30 phút (1800 giây)
    echo=config.debug_mode,
)


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_single_db():
    async with async_session() as db:
        return db