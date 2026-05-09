from fastapi import Depends,HTTPException,status 
from fastapi.security import OAuth2PasswordBearer
from jose import jwt ,JWTError
from sqlalchemy.orm import Session
from config.settings import setting
from app.database import get_db
from app.repositories.user import UserRepository
from app.auth.roles import ADMIN,STAFF,RECEPTION,MEDICAL

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

allowed_roles=["admin","doctor","receptionist"]
print(allowed_roles)

def get_current_user(token :str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token",
    headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token,setting.JWT_SECRET_KEY,
            algorithms=[setting.JWT_ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)

    if user is None:
        raise credential_exception

    return user

def require_role(allowed_roles: list[str]):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return current_user

    return role_checker