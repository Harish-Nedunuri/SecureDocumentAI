from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from fastapi.routing import APIRouter
from typing import Annotated
from ragcore.SupportUtils.secret_utils.config import get_settings
SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = get_settings().REFRESH_TOKEN_EXPIRE_DAYS


oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")
# Example users database
users_db = get_settings().USERS_DB

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

def verify_password(plain_password, hashed_password):
    #compare plain_password and hashed_password
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)
    

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user['hashed_password']):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
        
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter(
    tags=["AUTHENTICATION"],
    responses={404: {"description": "Not found"}}    
)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]    
):   
    username = form_data.username
    password = form_data.password
    user = authenticate_user(username, password)
    if not user:
       
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": username}, expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

router_refresh = APIRouter(
    tags=["AUTHENTICATION"],
    responses={404: {"description": "Not found"}}    
)
@router_refresh.post("/refresh-token", response_model=Token)
async def refresh_access_token(
    refresh_token: str = Form(...)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

router_success = APIRouter(    
    tags=["AUTHENTICATION"],
    responses={404: {"description": "Not found"}}    
)
@router_success.get("/sucess-endpoint")
async def auth_success_endpoint(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return {"message": f"Hello, {username}! Your access is granted."}



