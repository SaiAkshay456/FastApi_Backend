from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column,String,Text,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,relationship
from datetime import datetime
#all config related to database setup will be here

DB_URL="sqlite+aiosqlite:///./test.db"
# this above url is for testing purpose only
#if you want to use postgresql or other db then uncomment below line and provide your own credentials
#EX:DB_URL="postgresql+asyncpg://username:password@localhost/dbname"
#EX:DB_URL="postgresql+asyncpg://username:password@localhost/dbname"
class Base(DeclarativeBase):
    pass
#create data model
#extends DeclarativeBase to be recognized by sqlalchemy as data model
class User(Base):
    __tablename__="users"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    fullName=Column(String(100),nullable=False)
    email=Column(String(100),nullable=False,unique=True)
    password=Column(String(100),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)



#now create db
engine=create_async_engine(DB_URL)
async_sessionmaker=async_sessionmaker(engine,expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with async_sessionmaker() as session:
        yield session