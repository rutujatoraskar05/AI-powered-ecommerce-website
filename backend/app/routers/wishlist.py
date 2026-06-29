from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from dependencies.auth import get_current_user

from schemas.wishlist import WishlistCreate

from services.wishlist_service import (
    add_to_wishlist,
    get_wishlist,
    remove_wishlist_item
)

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)

@router.post("/add")
def add_item(
    item: WishlistCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = add_to_wishlist(
        db,
        current_user.user_id,
        item.product_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return {
        "message": "Added To Wishlist"
    }


@router.get("/")
def view_wishlist(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_wishlist(
        db,
        current_user.user_id
    )


@router.delete("/{wishlist_id}")
def remove_item(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    deleted = remove_wishlist_item(
        db,
        wishlist_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Wishlist Item Not Found"
        )

    return {
        "message": "Wishlist Item Removed"
    }