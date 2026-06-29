from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db

from schemas.category import (
    CategoryCreate,
    CategoryResponse
)

from services.category_service import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)
@router.post("/", response_model=CategoryResponse)
def add_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    return create_category(db, category)

@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    return get_all_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    category = get_category_by_id(
        db,
        category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )

    return category

@router.put("/{category_id}", response_model=CategoryResponse)
def edit_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    updated = update_category(
        db,
        category_id,
        category
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )

    return updated

@router.delete("/{category_id}")
def remove_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_category(
        db,
        category_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )

    return {
        "message": "Category Deleted Successfully"
    }