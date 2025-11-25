from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.security import hash_password, verify_password
from fastapi import HTTPException, status
from app.utils.email_utils import send_verification_email


class UserService:

    def create_user_with_password(self, db: Session, payload: UserCreate):
        try:
            data = payload.model_dump()
            safe_password = data["password"][:72]
            data["password_hash"] = hash_password(safe_password)
            del data["password"]  
            data["is_verified"] = False

            new_user = User(**data)

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            email_sent, token = send_verification_email(new_user.email)
            if not email_sent:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="User created but failed to send verification email"
                )

            return new_user

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )

    def authenticate_user(self, db: Session, email: str, password: str):
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user or not verify_password(password, user.password_hash):
                return None
            return user
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Authentication error: {str(e)}"
            )

    def get_by_email(self, db: Session, email: str):
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            raise HTTPException(500, f"Error retrieving user by email: {str(e)}")

    def get_all_users(self, db: Session):
        try:
            return db.query(User).all()
        except Exception as e:
            raise HTTPException(500, f"Error retrieving all users: {str(e)}")

    def get_user_by_id(self, db: Session, user_id: int):
        try:
            return db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            raise HTTPException(500, f"Error retrieving user by id: {str(e)}")

    def delete_user(self, db: Session, user_id: int):
        try:
            user = self.get_user_by_id(db, user_id)
            if not user:
                return False

            db.delete(user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error deleting user: {str(e)}")

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        try:
            user = self.get_user_by_id(db, user_id)
            if not user:
                return None

            update_data = user_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)
            return user

        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error updating user: {str(e)}")

    def verify_user(self, db: Session, email: str):
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return None

            user.is_verified = True
            db.commit()
            db.refresh(user)

            return user

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error verifying user: {str(e)}"
            )