from sqlalchemy.orm import Session
from models.user import User
from utils.security import hash_password
from models.user import User
from utils.security import verify_password

def register_user(db: Session, user_data):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        return None

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        mobile=user_data.mobile
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(
        db,
        email,
        password
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return user
