
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas,crud



router = APIRouter(
    prefix="/item_templates",
    tags=["ItemTemplates"]
)

# create item template (POST)
@router.post("/",response_model=schemas.ItemTemplateResponse,status_code=status.HTTP_201_CREATED)
async def create_item_template(item_template:schemas.ItemTemplateCreate,db:Session=Depends(get_db)):
    # check if template exists
    existing = crud.get_item_template_byname(db,item_template.name)
    if existing:
        raise HTTPException(status_code=400, detail="item template exists")
    existing = crud.get_item_template_bysku(db,item_template.sku)
    if existing:
        raise HTTPException(status_code=400, detail="item template exists")
    db_item_template = crud.create_item_template(db,item_template)
    return db_item_template

# get item template by id (GET)
@router.get("/{item_template_id}",response_model=schemas.ItemTemplateResponse)
async def read_item_template(item_template_id:int, db:Session=Depends(get_db)):
    db_item_template = crud.get_item_template(item_template_id=item_template_id,db=db)
    if not db_item_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"template with id {item_template_id} not found."
        )
    return db_item_template

# update (PUT)
@router.put("/{item_template_id}",response_model=schemas.ItemTemplateResponse)
async def update_item_template(item_template_id:int,
                               update_data:schemas.ItemTemplateUpdate,db:Session=Depends(get_db)):
    # check exist
    existing = crud.get_item_template(db,item_template_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"template with id {item_template_id} not found" )
    return crud.update_item_template(db,item_template_id,update_data)
    

# delete
@router.delete("/{item_template_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_template(item_template_id:int,db:Session=Depends(get_db)):
    result = crud.delete_item_template(db,item_template_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"item template with id {item_template_id} not found")
