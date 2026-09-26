from fastapi import HTTPException,Depends,APIRouter,status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas,crud
from app.utils.jwt import create_token


router = APIRouter(
    prefix="/auth",
    tags=["认证"]
)

# register (in auth all use post)
@router.post("/register",response_model=schemas.U)
def 