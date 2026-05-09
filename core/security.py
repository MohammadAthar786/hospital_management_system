from datetime import datetime, timedelta, timezone
# timedelta to add and subtract time 
# timezone->for using utc timezones 
from jose import jwt
# This library is for creating and verifying JWT tokens
## jwt.encode()->Creates JWT token
## jwt.decode()-> Verify/Read JWT token
from passlib.context import CryptContext
# password hashing Manager ->CryptContext 
## There are different Hashing Algorithms like bcrypt,argon2,pbkdf2 etc 
## CrypContext Manages them Professionaly


# password hashing setup
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
from dotenv import load_dotenv
import os 
load_dotenv(r"C:\Users\mohda\OneDrive\Desktop\health_record_system\.env")
# JWT secret key
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# JWT algorithm
ALGORITHM = os.getenv("JWT_ALGORITHM")
## JWT signing Method

# token expiry time
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

def hash_password(password: str) -> str:    
    return pwd_context.hash(password)
 


def verify_password(plain_password: str, hashed_password: str) -> bool:    
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:    
    to_encode = data.copy()    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    to_encode.update({"exp": expire})    
    encoded_jwt = jwt.encode(to_encode,        
                             SECRET_KEY,        
                             algorithm=ALGORITHM    
                             )    
    return encoded_jwt
