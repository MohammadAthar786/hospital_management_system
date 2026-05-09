from pydantic_settings import BaseSettings 
from dotenv import load_dotenv
from pathlib import Path

env_path=Path(__file__).resolve().parent.parent/".env"
load_dotenv(env_path)

class Setting(BaseSettings):
    JWT_SECRET_KEY:str
    JWT_ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
setting=Setting()
    