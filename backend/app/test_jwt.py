from utils.jwt_handler import *

token = create_access_token(
    {"sub": "rutuja@gmail.com"}
)

print("TOKEN:")
print(token)

print()

payload = verify_token(token)

print("PAYLOAD:")
print(payload)