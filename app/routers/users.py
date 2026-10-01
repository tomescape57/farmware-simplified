from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app import schemas,crud,models
from app.utils.dependencies import get_current_user


#----------------

router = APIRouter(
    prefix="/users",
    tags=["Users manage"]
)


# create user (POST
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    # check if user exists
    existing = crud.get_user_byname(db=db, username=user.username)
    if existing:
        raise HTTPException(status_code=400, detail="user exists")
    existing = crud.get_user_byemail(db=db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="user exists")
    return crud.create_user(db=db, user=user)
    


# get user by id (GET
@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id:int, db:Session=Depends(get_db)):
    db_user = crud.get_user(db=db,user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return db_user

# update user by id (PUT)
@router.put("/{user_id}",response_model=schemas.UserResponse)
async def update_user(user_id:int, update_data:schemas.UserUpdate, db:Session=Depends(get_db)):
    # check if user exists
    existing = crud.get_user(db,user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
            )
    return crud.update_user(db,user_id,update_data)

# update password
@router.put("/{user_id}/change-password")
def change_password(
    user_id: int,
    change_data: schemas.ChangePassword,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="只能修改自己的密码")
    result = crud.change_pswd(db, user_id, change_data)
    if result is None:
        raise HTTPException(status_code=400, detail="旧密码错误")
    return {"message": "密码修改成功"}


# delete user 
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int,db:Session=Depends(get_db)):
    # run and check exists
    result = crud.delete_user(db,user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    # 成功的话，什么都不返回，FastAPI 自动给 204
