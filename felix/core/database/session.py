from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os

DB_USER = "root"
DB_PASSWORD = str(os.getenv("MYSQL_ROOT_PASSWORD"))
DB_HOST = "db"
DB_PORT = "3306"
DB_NAME = str(os.getenv("MYSQL_DATABASE"))

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def database_session():
    ssession: Session = SessionLocal()
    try:
        yield ssession
    finally:
        ssession.close()
