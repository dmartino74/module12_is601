import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

# ✅ Import Base and engine from db
from app.db import Base, engine
# ✅ Import models so they are registered with Base.metadata
from app.models import calculation, user
# ✅ Import routers
from app.routes import users, calculations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Templates directory
templates = Jinja2Templates(directory="templates")

# ✅ Create tables at startup (ensures Calculation and User tables exist)
Base.metadata.create_all(bind=engine)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(status_code=400, content={"error": error_messages})

# Root template
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Added hello_world endpoint for E2E tests
@app.get("/hello_world")
async def hello_world():
    return {"message": "Hello World"}

# ✅ Healthcheck endpoint for Docker
@app.get("/health")
async def health():
    return {"status": "ok"}

# ✅ Include routers
# IMPORTANT: calculations router already has prefix="/calculate" inside its file
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(calculations.router, tags=["calculations"])
