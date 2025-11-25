from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user_schema import UserUpdate, UserResponse
from app.services.user_service import UserService
from app.deps.auth_deps import get_current_user, require_roles

router = APIRouter()
user_service = UserService()


# Get current user
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


# Admin: Get all users
@router.get("/all", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin"))
):
    return user_service.get_all_users(db)


# Get user by ID (self or admin)
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Access control
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Unauthorized")

    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user


# Update user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Unauthorized")

    updated = user_service.update_user(db, user_id, payload)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return updated


# Admin: delete a user
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin"))
):
    deleted = user_service.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return {"message": "User deleted successfully"}
