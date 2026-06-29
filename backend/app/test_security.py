from utils.security import *

password = "123456"

hashed = hash_password(password)

print("Hashed Password:")
print(hashed)

print()

print(
    verify_password(
        "123456",
        hashed
    )
)