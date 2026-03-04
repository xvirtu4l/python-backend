import os
from datetime import datetime, timedelta, timezone
from config.settings import get_settings
from typing import Dict, Any

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

settings = get_settings()
jwt_config = settings.jwt

def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_config.access_token_expire_minutes)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, jwt_config.secret_key, algorithm=jwt_config.algorithm)
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    try:
        decoded_payload = jwt.decode(token, jwt_config.secret_key, algorithms=[jwt_config.algorithm])
        return decoded_payload
    except InvalidTokenError:
        raise InvalidTokenError("Token không hợp lệ hoặc đã hết hạn")
    
def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        payload = decode_token(token)
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
        )