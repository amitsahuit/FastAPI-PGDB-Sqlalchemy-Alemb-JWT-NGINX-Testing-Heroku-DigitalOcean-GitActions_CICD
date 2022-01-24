from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""-----------------------------DB Operations without SQL Alchemy----------------------------------"""
# import psycopg2
# from psycopg2.extras import RealDictCursor

# try:
#     conn = psycopg2.connect(host='localhost',dbname='fastapidb1', user='postgres',password='sys', cursor_factory=RealDictCursor)
#     cur = conn.cursor()
#     print("DB connection is successful")
#     cur.fetchone()
#     cur.close()
#     conn.close()
# except Exception as error:
#     print("Error is: ",error)


"""-----------------------------DB Operations with SQL Alchemy----------------------------------"""
from .config import setting
#SQLALCHEMY_DATABASE_URL = "postgresql://<userName>:<password>@<IP address>/<db name>"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sys@localhost:5432/fastapidb1"
SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#For SQlLite-->
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()