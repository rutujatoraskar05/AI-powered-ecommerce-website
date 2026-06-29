from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.product_service import search_products
from services.product_service import filter_products
from database.db import get_db

from schemas.product import (
    ProductCreate,
    ProductResponse
)

from services.product_service import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product)


@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    return get_all_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def edit_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    updated = update_product(
        db,
        product_id,
        product
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

    return updated


@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    try:
        deleted = delete_product(db, product_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Product Not Found"
            )

        return {
            "message": "Product Deleted Successfully"
        }

    except Exception as e:
        return {"error": str(e)}
    
@router.get("/search/")
def search_product(
    keyword: str,
    db: Session = Depends(get_db)
):

    return search_products(
        db,
        keyword
    )

@router.get("/filter/")
def filter_product(
    min_price: float = None,
    max_price: float = None,
    brand: str = None,
    db: Session = Depends(get_db)
):

    return filter_products(
        db,
        min_price,
        max_price,
        brand
    )

from services.product_service import (
    search_products,
    filter_products
)

@router.get("/search")
def search(
    keyword: str,
    db: Session = Depends(get_db)
):

    return search_products(
        db,
        keyword
    )

@router.get("/filter")
def filter_product(
    brand: str = None,
    min_price: float = None,
    max_price: float = None,
    db: Session = Depends(get_db)
):

    return filter_products(
        db,
        brand,
        min_price,
        max_price
    )