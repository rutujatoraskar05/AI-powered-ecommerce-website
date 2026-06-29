from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.db import get_db

from dependencies.auth import get_current_user

from schemas.review import ReviewCreate

from services.review_service import (
    add_review,
    get_reviews
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/")
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    review = add_review(
        db,
        current_user.user_id,
        data.product_id,
        data.rating,
        data.comment
    )

    return review


@router.get("/{product_id}")
def product_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):

    return get_reviews(
        db,
        product_id
    )