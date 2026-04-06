import os
from dotenv import load_dotenv
load_dotenv()

def get_db_uri() -> str:
    POSTGRES_SERVER = os.getenv('POSTGRES_SERVER', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'gpt_teacher')
    
    DB_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode=disable"
    return DB_URI