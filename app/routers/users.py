from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app import schemas,crud


#----------------

router = APIRouter(
    prefix="/users",
    tags=["Users manage"]
)


# create user (POST
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(_user:schemas.UserCreate, _db:Session=Depends(get_db)):
    # check if user exists
    existing = crud.get_user_byname(db=_db, username=_user.username)
    if existing:
        raise HTTPException(status_code=400, detail="user exists")
    existing = crud.get_user_byemail(db=_db, email=_user.email)
    if existing:
        raise HTTPException(status_code=400, detail="user exists")
    return crud.create_user(db=_db, user=_user)
    


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
async def update_user(user_id:int, update_data:schemas.UserUpdate, _db:Session=Depends(get_db)):
    # check if user exists
    existing = crud.get_user(_db,user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
            )
    return crud.update_user(_db,user_id,update_data)

# update password



# delete user 
@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int,_db:Session=Depends(get_db)):
    # run and check exists
    result = crud.delete_user(_db,user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    # 成功的话，什么都不返回，FastAPI 自动给 204
