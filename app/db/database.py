from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.DB_ECHO,  # Loguea todas las consultas SQL
    pool_pre_ping=True,  # Hace un ping a la conexion antes de usarla
    pool_size=5,  # Conexiones persistentes que mantiene el pool
    max_overflow=10,  # Conexiones extra temporales
    pool_recycle=1800,  # Recicla conexiones a los 30 min
)

async_session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
