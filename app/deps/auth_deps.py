from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status
from jose import jwt,JWTError

from app.database.database import get_db
from app.models.user_model import User
from app.utils.security import JWT_SECRET_KEY, JWT_ALGORITHM

oauth2_scheme = HTTPBearer()


def get_current_user(token: str = Depends(oauth2_scheme),db=Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        role = payload.get("role")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        user.role = role 
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_roles(*roles):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return role_checker
