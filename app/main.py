from fastapi import FastAPI,HTTPException,Depends,UploadFile,File
# from app.schema import User,Post
from app.db import User,create_db_and_tables,get_async_session
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import UserCreate
from sqlalchemy import select
from app.images import imageKitClient

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield
app=FastAPI(lifespan=lifespan) 


@app.post("/create/user")
async def createUser(user:UserCreate,session:AsyncSession=Depends(get_async_session)):
    stmt=select(User).where(User.email==user.email)
    execute_stmt=await session.execute(stmt)
    existing_user=execute_stmt.scalar_one_or_none()
    if existing_user:
        return HTTPException(
            status_code=402,
            detail=f"{user.email} already exists"
        )
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

@app.post("/upload/file")
async def uploadFile(
    file:UploadFile=File(...),#required alsi file:UploadFile | None=File() optional category this
    session:AsyncSession=Depends(get_async_session)):
    response = imageKitClient.upload(
        file=file.file,
        file_name=file.filename
    )
    return {
        "url": response["url"],
        "thumbnail": response["thumbnailUrl"],
        "fileId": response["fileId"]
    }
