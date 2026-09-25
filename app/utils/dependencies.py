from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.utils.jwt import decode_token
from app.database import get_db
from app import crud,models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(
    token:str = Depends(oauth2_scheme),
    db:Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401,detail="token format error")
    except Exception:
        raise HTTPException(status_code=401,detail="token invalid or expired")

    db_user = crud.get_user(db=db,user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=401,detail="user not exist")
    return db_user


def require_role(required_roles:List[str]): # Currying function!
    def role_checker(current_user:models.User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"lack permission, need be one of: {','.join(required_roles)}")
        return current_user
    return role_checker

# pre define common dependencies
require_admin = require_role(["admin"])
require_manager_or_admin = require_role(["admin,manager"])