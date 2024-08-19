from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class Token(BaseModel):
    access_token: str
    token_type: str
