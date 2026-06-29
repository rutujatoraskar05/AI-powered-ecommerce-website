from schemas.user import UserCreate
from schemas.product import ProductCreate

user = UserCreate(
    name="Rutuja",
    email="rutuja@gmail.com",
    password="123456",
    mobile="9876543210"
)

print(user)