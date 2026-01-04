from fastapi import FastAPI,HTTPException,Depends
# from app.schema import User,Post
from app.db import User,create_db_and_tables,get_async_session
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import UserCreate
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield
app=FastAPI(lifespan=lifespan) 


@app.post("/create/user")
async def createUser(user:UserCreate,session:AsyncSession=Depends(get_async_session)):
    new_user=User(
        fullName=user.fullName,
        email=user.email,
        password=user.password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@app.get("/get/users")
async def get_all_users(session:AsyncSession=Depends(get_async_session)):
    users=await session.execute(select(User))
    return users.scalars().all()
