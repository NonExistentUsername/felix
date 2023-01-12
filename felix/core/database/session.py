from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URI = str(os.getenv("DATABASE_URI"))

connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)