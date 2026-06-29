from fastapi import Depends
from fastapi import HTTPException

from dependencies.auth import get_current_user


def get_admin_user(
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin Access Required"
        )

    return current_user