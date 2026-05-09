from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.database import get_db
from app.services.auth import AuthService
from app.schemas.auth import UserRegister, UserLogin, UserResponse, Token
from app.auth.roles import (
    ADMIN,
    STAFF,
    RECEPTION,
    MEDICAL
)
from dependencies.auth import get_current_user, require_role

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(data: UserRegister,db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register_user(data)


@router.post("/login",response_model=Token)
def login_user(data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_user(email=data.username,
                              password=data.password)

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


@router.get("/admin-only")
def admin_only(current_user = Depends(require_role(["admin"]))):
    return {
        "message": "Welcome admin",
        "user": current_user.email
    }