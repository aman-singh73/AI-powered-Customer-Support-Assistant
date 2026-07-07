import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Use lowercase or uppercase from env, fallback to localhost for local testing
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("database_url") or "postgresql://postgres:postgres@localhost:5433/support_db"

# Replace 'db' with 'localhost' if running locally outside docker network
if "@db:" in SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("@db:", "@localhost:")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
