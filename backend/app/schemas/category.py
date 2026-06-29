from pydantic import BaseModel


class CategoryCreate(BaseModel):
    category_name: str


class CategoryResponse(CategoryCreate):
    category_id: int

    class Config:
        from_attributes = True