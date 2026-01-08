from fastapi import FastAPI,HTTPException,Depends,UploadFile,File
# from app.schema import User,Post
from app.db import User,create_db_and_tables,get_async_session
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import UserCreate
from sqlalchemy import select
from app.images import imageKitClient
import math
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

def format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
@app.post("/upload/file")
async def uploadFile(
    file:UploadFile=File(...),#required alsi file:UploadFile | None=File() optional category this
    session:AsyncSession=Depends(get_async_session)):
    filename = file.filename
    mimetype = file.content_type
    size_in_bytes = file.size
    sizeReadable=format_size(size_in_bytes)
    try:
        file_content = await file.read()
        upload_result = imageKitClient.files.upload(
            file=file_content,
            file_name=file.filename,
            use_unique_file_name=True, 
            folder="/uploads/"
        )
        return {
            "message": "Upload successful",
            "url": upload_result.url,
            "file_id": upload_result.file_id,
            "thumbnail": upload_result.thumbnail_url,
            "file_metaData":{
                "name":filename,
                "file_type":mimetype,
                "size":size_in_bytes,
                "readAbleSize":sizeReadable
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))