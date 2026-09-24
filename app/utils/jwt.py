import jwt
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException

SECRET_KEY = "testkeytestkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_token(user_id:int,role:str):
    payload={
        "user_id":user_id,
        "role":role, # write role
        "exp":datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # expire in 2 hours
    }
    token=jwt.encode(payload,SECRET_KEY,ALGORITHM)
    return token

def decode_token(token:str) -> dict:
    # return dictionary of payload
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token.")

