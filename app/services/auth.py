from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.schemas.auth import UserRegister, UserLogin
from core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, data: UserRegister):
        existing_user = self.user_repo.get_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_data = {
            "email": data.email,
            "hashed_password": hash_password(data.password),
            "role": data.role
        }

        return self.user_repo.create(user_data)

    def login_user(self,email:str,password:str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        access_token = create_access_token(
            data={
                "sub": user.email,
                "role": user.role
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }