from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas,crud
from app.utils.jwt import create_token
from app.utils.security import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["认证authentication"]
)

# register (in auth all use post)
@router.post("/register",response_model = schemas.UserResponse, status_code = status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate,db:Session=Depends(get_db)):
    # check if exist username
    existing_user = crud.get_user_byname(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400,detail="username already exists")
    # check if exist email
    existing_email = crud.get_user_byemail(db,user_data.email)
    if existing_email:
        raise HTTPException(status_code=400,detail="email already registered")
    # create user
    new_user = crud.create_user(db,user_data)
    return new_user


# login
@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # 根据用户名或邮箱查找用户
    user = crud.get_user_byname_oremail(db, login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证密码
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成 token
    access_token = create_token(user_id=user.id, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}