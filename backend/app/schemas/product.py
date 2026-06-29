from pydantic import BaseModel

class ProductCreate(BaseModel):

    product_name: str
    brand: str
    description: str
    price: float
    stock: int
    image_url: str
    category_id: int


from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_name: str
    brand: str
    description: str
    price: float
    stock: int
    image_url: str
    category_id: int


class ProductResponse(ProductCreate):

    product_id: int

    class Config:
        from_attributes = True