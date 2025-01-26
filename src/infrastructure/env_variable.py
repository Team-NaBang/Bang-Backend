from dotenv import load_dotenv
import os

load_dotenv()

AUTHENTICATION_CODE = os.getenv("AUTHENTICATION_CODE")
DATABASE_URL = os.getenv("DATABASE_URL")
CLIENT_DOMAIN = os.getenv("CLIENT_DOMAIN")
SERVER_ENV = os.getenv("SERVER_ENV", "Development")