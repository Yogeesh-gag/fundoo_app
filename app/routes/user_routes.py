from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Dict

from app.database.database import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.deps.auth_deps import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/getallusers",
            response_model=List[UserResponse],
            dependencies=[Depends(require_roles("admin"))])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)


@router.get("/getuser/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(403, "Unauthorized")

    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    return user
