import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from pydantic import field_validator
from fastapi import FastAPI, HTTPException, Depends
from typing import Optional,Dict,List,Any
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json

env_path = Path(".") / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
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
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    USER_AGENT: bool = os.getenv('USER_AGENT',default=False)
    ALGORITHM: str = os.getenv('ALGORITHM',default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',default=15)
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS',default=7)
    # Users DB
    USERS_DB: Dict[str, Dict[str, str]] = os.getenv('USERS_DB',default={})
   
    
def get_settings() -> Settings:
    return Settings()