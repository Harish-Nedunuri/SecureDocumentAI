from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib
from ragcore.EmbeddingsLLM.router import router as fine_tune_llm
from ragcore.QueryPromptTask.router import router as docu_prompt_task,multi_router
from fastapi.templating import Jinja2Templates
import pkg_resources
from ragcore.SupportUtils.security_utils.oauth2_security import router as oauth2_router,router_success,router_refresh,oauth2Scheme


package_name = 'ragcore'  # Replace with the package you want to check
version = pkg_resources.get_distribution(package_name).version

BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI(title="Secure Document API",version=version,description="API for document management, advanced OCR and text analytics")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home_view(request: Request):
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
    return templates.TemplateResponse("home.html", {"request": request,"status": "Running!"})

# OAuth2 Security
app.include_router(oauth2_router)
app.include_router(router_refresh)
app.include_router(router_success)

# Setup where your static files are located
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# FineTuneLLM Endpoints
app.include_router(fine_tune_llm)

# DocuPromptTask Endpoints
app.include_router(docu_prompt_task)
# DocuPromptTask Endpoints
app.include_router(multi_router)




