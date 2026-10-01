
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas,crud

router = APIRouter(
    prefix="/inventorys",
    tags=["Inventories"]
)



# create 1 inventory data
@router.post("/",response_model=schemas.InventoryResponse,status_code=status.HTTP_201_CREATED)
async def create_inventory(inventory:schemas.InventoryCreate,db:Session=Depends(get_db)):
    template = crud.get_item_template(
        db=db,
        item_template_id=inventory.template_id,
    )
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item template with id {inventory.template_id} not found",
        )
    db_inventory = crud.create_inventory(db=db, inventory=inventory)
    return db_inventory
    
# read inventory by id
@router.get("/{inventory_id}",response_model=schemas.InventoryResponse)
async def read_inventory(inventory_id:int,db:Session=Depends(get_db)):
    db_inventory = crud.get_inventory(db,inventory_id)
    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"inventory with id {inventory_id} not found"
        )
    return db_inventory

# update inventory
@router.put("/{inventory_id}",response_model=schemas.InventoryResponse)
async def update_inventory(inventory_id:int,
                           update_data:schemas.InventoryUpdate,
                           db:Session=Depends(get_db)):
    # check existance
    existing = crud.get_inventory(db,inventory_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"inventory with id {inventory_id} not found"
        )
    return crud.update_inventory(db,inventory_id,update_data)

# delete inventory
@router.delete("/{inventory_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(inventory_id:int,db:Session=Depends(get_db)):
    result = crud.delete_inventory(db,inventory_id)
    if result == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"inventory with id {inventory_id} not found"
        )