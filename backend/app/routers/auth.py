from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from schemas.user import UserLogin
from schemas.user import UserUpdate
from schemas.user import PasswordChange
from services.auth_service import login_user
from utils.jwt_handler import create_access_token
from dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from models.user import User
from utils.security import hash_password
from utils.security import verify_password

from database.db import get_db

from schemas.user import UserCreate

from services.auth_service import register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    created_user = register_user(
        db,
        user
    )

    if created_user is None:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return {
        "message": "User Registered Successfully",
        "user_id": created_user.user_id
    }

@router.post("/login")
def login(
        user: UserLogin,
        db: Session = Depends(get_db)
):

    db_user = login_user(
        db,
        user.email,
        user.password
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

from dependencies.auth import get_current_user

from dependencies.auth import get_current_user

@router.get("/me")
def get_profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Protected Route",
        "user": current_user
    }


@router.put("/me")
def update_profile(
    profile: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing = db.query(User).filter(
        User.email == profile.email,
        User.user_id != current_user.user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    current_user.name = profile.name
    current_user.email = profile.email
    current_user.mobile = profile.mobile

    db.commit()
    db.refresh(current_user)

    token = create_access_token(
        {
            "sub": current_user.email
        }
    )

    return {
        "message": "Profile Updated Successfully",
        "user": current_user,
        "access_token": token
    }


@router.put("/change-password")
def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    current_user.password = hash_password(payload.new_password)
    db.commit()

    return {
        "message": "Password Changed Successfully"
    }
