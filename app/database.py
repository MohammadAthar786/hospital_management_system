from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent / ".env"
print(env_path)
print(env_path.exists())

load_dotenv(env_path)


DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_NAME     = os.getenv("DB_NAME", "health_db")
DB_USER     = os.getenv("DB_USER", "postgres")
from urllib.parse import quote_plus
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(DATABASE_URL)

# Engine = the actual connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal = a factory that creates DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = parent class all your models will inherit from
Base = declarative_base()


# This is a dependency — FastAPI will call this automatically
# for every request, give it a DB session, then close it after
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()