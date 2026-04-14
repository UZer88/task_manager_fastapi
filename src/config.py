import os
from dotenv import load_dotenv

load_dotenv()

# База данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./task_manager.db")

# JWT настройки
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30