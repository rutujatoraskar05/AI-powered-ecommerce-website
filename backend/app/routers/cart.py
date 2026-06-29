from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db

from schemas.cart import AddToCart

from services.cart_service import (
    add_to_cart,
    get_cart,
    remove_cart_item,
    clear_cart
)

from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/add")
def add_product_to_cart(
    item: AddToCart,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart_item = add_to_cart(
        db,
        current_user.user_id,
        item.product_id,
        item.quantity
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return {
        "message": "Product Added To Cart"
    }


@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_cart(
        db,
        current_user.user_id
    )


@router.delete("/remove/{cart_item_id}")
def remove_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    deleted = remove_cart_item(
        db,
        cart_item_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Item Not Found"
        )

    return {
        "message": "Item Removed Successfully"
    }


@router.delete("/clear")
def empty_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    clear_cart(
        db,
        current_user.user_id
    )

    return {
        "message": "Cart Cleared Successfully"
    }

