from sqlalchemy import Column, Integer, String, Boolean
from app.database.settings import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    age = Column(Integer)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="user")
