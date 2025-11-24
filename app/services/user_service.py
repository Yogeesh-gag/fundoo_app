from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password, verify_password


class UserService:

    def create_user_with_password(self, db: Session, payload: UserCreate):
        safe_password = payload.password[:72]
        hashed = hash_password(safe_password)

        new_user = User(
            name=payload.name,
            email=payload.email,
            password_hash=hashed,
            age=payload.age,
            role=payload.role,
            is_verified=False
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def authenticate_user(self, db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user_by_id(db, user_id)
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True

    def update_user(self, db: Session, user_id, user_update):
        user = self.get_user_by_id(db, user_id)
        if not user:
            return None
        user.name = user_update.name
        user.email = user_update.email
        user.age = user_update.age
        db.commit()
        db.refresh(user)
        return user
