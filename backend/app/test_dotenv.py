from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv("GROQ_API_KEY"))
