from sqlalchemy.orm import Session
from app import models,schemas
from app.utils import security

# user crud operations
def create_user(db: Session, user: schemas.UserCreate):
    # create sqlAlchemy object , from the schema template to db model
    db_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = security.get_password_hash(user.password),
        role = user.role
    )
    # add object to session
    db.add(db_user)
    # write to real db
    db.commit()
    # refresh object, let db return id and so on to python
    db.refresh(db_user)
    # get the db object (fastapi will use pydantic to turns obj to json)
    return db_user

    # get user by id
def get_user(db:Session,user_id:int):
    # using sqlalchemy  query grammar
    return db.query(models.User).filter(models.User.id == user_id).first()
def get_user_byname(db:Session,username:str):
    return db.query(models.User).filter(models.User.username == username).first()
def get_user_byemail(db:Session,email:str):
    return db.query(models.User).filter(models.User.email == email).first()
def get_user_byname_oremail(db:Session,identifier:str):
    user = db.query(models.User).filter(
        (models.User.username == identifier)|
        (models.User.email == identifier)
    ).first()
    return user

def update_user(db:Session, user_id:int, update_data: schemas.UserUpdate):
    # find the user to update
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    # take non None field(字段?) only, from input user_update
    update_data = update_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def change_pswd(db:Session,user_id:int,change_pswd: schemas.ChangePassword):
    # check user item
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        return None
    # take current pswd and compare with inputed old password
    if not security.verify_password(change_pswd.old_password,db_user.hashed_password):
        return None
    # hash the new pswd and write
    db_user.hashed_password = security.get_password_hash(change_pswd.new_password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session,user_id:int):
    # find and check existance 
    db_user = db.query(models.User).filter(models.User.id==user_id).first() # when call db, there is a tracker added to the var by (sqlalchemy?)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return True




# item template crud
def create_item_template(db:Session, item_template: schemas.ItemTemplateCreate):
    db_item_template = models.ItemTemplate(
        name = item_template.name,
        sku = item_template.sku,
        description = item_template.description,
        unit = item_template.unit
    )
    db.add(db_item_template)
    db.commit()
    # let db return id, etc...
    db.refresh(db_item_template)
    return db_item_template

def get_item_template(db:Session, item_template_id:int):
    return db.query(models.ItemTemplate).filter(models.ItemTemplate.id == item_template_id).first()
def get_item_template_byname(db:Session, item_template_name:str):
    return db.query(models.ItemTemplate).filter(models.ItemTemplate.name == item_template_name).first()
def get_item_template_bysku(db:Session, item_template_sku:str):
    return db.query(models.ItemTemplate).filter(models.ItemTemplate.sku == item_template_sku).first()

def update_item_template(db:Session, template_id:int,update_data:schemas.ItemTemplateUpdate):
    db_template = db.query(models.ItemTemplate).filter(models.ItemTemplate.id==template_id).first()
    if not db_template: return None
    # take non none data only
    update_data = update_data.model_dump(exclude_unset=True)
    for field,value in update_data.items():
        setattr(db_template,field,value)
    db.commit()
    db.refresh(db_template)
    return db_template

def delete_item_template(db:Session,template_id:int):
    db_item_template = db.query(models.ItemTemplate).filter(models.ItemTemplate.id==template_id).first()
    if not db_item_template:
        return None
    db.delete(db_item_template)
    db.commit()
    return True



# inventory item (inventory) crud
def create_inventory(db:Session, inventory:schemas.InventoryCreate):
    db_inventory = models.Inventory(
        template_id = inventory.template_id,
        quantity = inventory.quantity
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db:Session, inventory_id:int):
    return db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()




# Logs CRUD (Read Only)

# 1. 获取某个特定库存的所有操作历史（最常用）
def get_inventory_logs_by_item(db: Session, inventory_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.InventoryLog)
        .filter(models.InventoryLog.inventory_id == inventory_id)
        .order_by(models.InventoryLog.time_stamp.desc()) # 最新的操作排在最前面
        .offset(skip)
        .limit(limit)
        .all()
    )

# 2. 获取某个特定模板的所有操作历史
def get_template_logs_by_item(db: Session, template_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.TemplateLog)
        .filter(models.TemplateLog.template_id == template_id)
        .order_by(models.TemplateLog.time_stamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

# 3. 获取全局日志列表（通常只有 Admin 才能看）
def get_all_inventory_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InventoryLog).order_by(models.InventoryLog.time_stamp.desc()).offset(skip).limit(limit).all()