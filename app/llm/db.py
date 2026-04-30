from app.core.config import settings

def get_db_uri() -> str:
    POSTGRES_SERVER = settings.POSTGRES_SERVER
    POSTGRES_PORT = settings.POSTGRES_PORT
    POSTGRES_USER = settings.POSTGRES_USER
    POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
    POSTGRES_DB = settings.POSTGRES_DB
    
    DB_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode=disable"
    return DB_URI