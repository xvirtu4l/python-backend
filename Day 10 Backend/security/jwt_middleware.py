from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette import status

from security.jwt_service import decode_token
from security.token_blacklist import blacklisted_tokens

PUBLIC_PATHS = {
    "/api/auth/login",
    "/api/auth/forgot-password",
    "/api/auth/reset-password",
    "/users/create",
    "/docs", 
    "/openapi.json", 
    "/redoc",
    "/"
}

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if request.method == "OPTIONS":
            return await call_next(request)
        
        if path in PUBLIC_PATHS:
            response = await call_next(request)
            return response
        
        auth_header = request.headers.get("authorization")
        # print("DEBUG: JWTMiddleware - Authorization header:", request.headers.get("authorization"))
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing Authorization Header"}
            )
            
        token = auth_header.split(" ", 1)[1]
        
        if token in blacklisted_tokens:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token has been blacklisted"}
            )
        
        try:
            payload = decode_token(token)
            # print("DEBUG: JWTMiddleware - payload:", payload)
            request.state.user = payload
        except Exception as e:
            # print("DEBUG: JWTMiddleware - decode error:", e)
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"}
            )
        
        return await call_next(request)
