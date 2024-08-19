from fastapi import FastAPI, HTTPException, Depends, Query,Body,Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib
from ragcore.EmbeddingsLLM.router import router as fine_tune_llm
from ragcore.DocuPromptTask.router import router as docu_prompt_task,multi_router
from fastapi.templating import Jinja2Templates
from ragcore.CommonCore.secret_utils.config import get_settings
import pkg_resources
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from ragcore.CommonCore.security_utils.oauth2_security import Token

package_name = 'ragcore'  # Replace with the package you want to check
version = pkg_resources.get_distribution(package_name).version

BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI(title="AI for Document Management API",version=version,description="API for document management, advanced OCR and text analytics")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home_view(request: Request):
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
    return templates.TemplateResponse("home.html", {"request": request,"status": "Running!"})

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Replace this with your actual authentication logic
    if form_data.username != "user" or form_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": form_data.username, "token_type": "bearer"}


# Setup where your static files are located
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# FineTuneLLM Endpoints
app.include_router(fine_tune_llm)

# DocuPromptTask Endpoints
app.include_router(docu_prompt_task)
# DocuPromptTask Endpoints
app.include_router(multi_router)




