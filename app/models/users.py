from uuid import UUID
from sqlalchemy import Column,String,Boolean,DateTime
from sqlalchemy.sql import func
# For using database side functions like NOW(),AVG(),COUNT(),SUM(),MAX(),MIN()
# for example func.now()
from sqlalchemy.dialects.postgresql import UUID
## --(dialects)-- means DB specific features--SQLAlchemy is Generic ORM Different DBs has 
## Different capabilities

## This line is just importing PostGreSQL specific datatype UUID
## IN PostGresSQL UUID is actual datatype 
## Why we even importing it Problem we might face without this?

## let's say we do id=Column(String)  --> In SQL id will store as  (VARCHAR)
## so technically UUID may be stored as text but that is inefficient,validation weak,PostGres Optimization Miss
## Indexing less optimized 
import uuid 
# Built in module of python used ro generate unique IDs
## example -550e8400-e29b-41d4-a716-446655440000
##-- we are using UUIDs instead of simple integer IDs
## because that is more Secure ,globally unique,common in production system,can't be guessed
## There are mutiple versions to generate  UUID most common is 
### print(uuid.uuid4())-->This Randomly generate UUID(Universally Unique Identifier)
from app.database import Base

class User(Base):
    __tablename__="user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False, default="patient")

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())