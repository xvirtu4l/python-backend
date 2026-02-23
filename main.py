from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.exceptions import BusinessError, DuplicateUserError
from api.user_router import router as user_router
from api.auth_router import router as auth_router
from security.jwt_middleware import JWTMiddleware

app = FastAPI(title="Quản lý người dùng")
app.add_middleware(JWTMiddleware)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")

def root():
    return {"message": "Hello, World!"}

@app.exception_handler(BusinessError)
def bussiness_exception_handler(request: Request, exc: BusinessError):
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