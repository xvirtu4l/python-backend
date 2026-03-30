from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings
from domain.exceptions import BusinessError, DuplicateUserError
from api.user_router import router as user_router
from api.auth_router import router as auth_router
from api.file_router import router as file_router
from api.chatbot_router import router as chatbot_router
from security.jwt_middleware import JWTMiddleware
import traceback

settings = get_settings()
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

if settings.frontend_url not in allowed_origins:
    allowed_origins.append(settings.frontend_url)

app = FastAPI(title="Quản lý người dùng")

app.add_middleware(JWTMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(file_router)
app.include_router(chatbot_router)

@app.get("/")

def root():
    return {"message": "Hello, World!"}

@app.exception_handler(BusinessError)
def business_exception_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )
    
@app.exception_handler(DuplicateUserError)
def duplicate_user_exception_handler(request: Request, exc: DuplicateUserError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )
    
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Print full traceback to console for debugging
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
