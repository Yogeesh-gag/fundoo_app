from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.database.database import db
from app.utils.email_utils import confirm_token
from app.services.user_service import UserService


router=APIRouter()
user_service=UserService()

@router.get("/confirm",status_code=200)
def verify_email(token: str,db:Session=Depends(db.get_db)):
    email=confirm_token(token)
    print("TOKEN EMAIL:",email)
    if not email:
        raise HTTPException(status_code=400,detail="Invalid or expired token")
    
    user= user_service.verify_user(db,email)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    return {"message":"Email verified successfully",
            "email":user.email,
            "is_verified":user.is_verified
    }
