

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, Integer
from pgvector.sqlalchemy import Vector

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5439/seeai_rag"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class DocumentModel(Base):
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list] = mapped_column(Vector(384), nullable=False)