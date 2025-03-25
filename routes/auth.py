from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, TokenResponse
from core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# User Signup
@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, password_hash=hashed_pwd, role='user')
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    
    return new_user

# User Login
@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}