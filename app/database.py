from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL="postgresql://postgres:123456@localhost:5432/learn_db"
engine=create_engine(DB_URL)
session=sessionmaker(autocommit=False,autoflush=False,bind=engine)