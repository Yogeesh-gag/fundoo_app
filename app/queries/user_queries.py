from app.models.user_model import User


class UserQueries:
    @staticmethod
    def get_all(db):
        return db.query(User).all()

    @staticmethod
    def get_by_id(db, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(db, user_data):
        user = User(**user_data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db, user, user_update):
        user.name = user_update.name
        user.email = user_update.email
        user.age = user_update.age
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db, user):
        db.delete(user)
        db.commit()
        return True