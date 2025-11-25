from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth_schema import LoginSchema
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService
from app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
user_service = UserService()


@router.post("/register", response_model=UserResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = user_service.get_by_email(db, payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = user_service.create_user_with_password(db, payload)
        return user

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during registration: {str(e)}"
        )


@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    try:
        user = user_service.authenticate_user(db, payload.email, payload.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token(user)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )
