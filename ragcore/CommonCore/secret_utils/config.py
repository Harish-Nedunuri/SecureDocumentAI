import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
env_path = Path(".") / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Dependency for token authentication
def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    # Static token for authentication
    STATIC_TOKEN = get_settings().AUTH_TOKEN
    print(STATIC_TOKEN)
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")
    return credentials.credentials

class Settings(BaseSettings):    
    # Database
    DB_USER: str = os.getenv('MSSQL_USER')
    DB_PASSWORD: str = os.getenv('MSSQL_PASSWORD')
    DB_NAME: str = os.getenv('MSSQL_DB')
    DB_HOST: str = os.getenv('MSSQL_SERVER')
    DB_PORT: str = os.getenv('MSSQL_PORT')
    DATABASE_URL: str = f'mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server'
    AFR_ENDPOINT: str = os.getenv('AFR_ENDPOINT')
    DEBUG: bool = os.getenv('DEBUG')
    AFR_KEY: str = os.getenv('AFR_KEY')
    AFR_MODEL_ID: str = os.getenv('AFR_MODEL_ID')
    STORAGE_ACCOUNT_NAME: str = os.getenv('STORAGE_ACCOUNT_NAME')
    STORAGE_ACCOUNT_KEY: str = os.getenv('STORAGE_ACCOUNT_KEY')
    STORAGE_CONNECTION_STRING: str = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    AUTH_TOKEN: str = os.getenv('AUTH_TOKEN')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    USER_AGENT: bool = os.getenv('USER_AGENT')

   
    
def get_settings() -> Settings:
    return Settings()