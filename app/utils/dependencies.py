from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.jwt import decode_token
from app.database import get_db
from app import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(
    token:str = Depends(oauth2_scheme),
    db:Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        _user_id = payload.get("user_id")
        if not _user_id:
            raise HTTPException(status_code=401,detail="token format error")
    except Exception:
        raise HTTPException(status_code=401,detail="token invalid or expired")

    db_user = crud.get_user(db=db,user_id=_user_id)
    if not db_user:
        raise HTTPException(status_code=401,detail="user not exist")
    return db_user