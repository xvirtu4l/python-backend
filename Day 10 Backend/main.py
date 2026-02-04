from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.exceptions import BusinessError, DuplicateUserError
from api.user_router import router

app = FastAPI(title="Quản lý người dùng")

app.include_router(router)

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