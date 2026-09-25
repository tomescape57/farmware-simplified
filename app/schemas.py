
# 第一步：永远从这里开始，导入 Pydantic 的 BaseModel
# schemas classes are for data validation, like a filter
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.types import UserRole
from app.utils import security


# 1. User 相关的 Schemas
# 基础类：把 Create 和 Response 共有的字段抽出来，减少重复代码
class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr  # Pydantic 会自动验证这是否是一个合法的邮箱格式
    role: UserRole

# pwd separated
class UserCreate(UserBase):
    password: str = Field(min_length=8,max_length=25)  

class UserUpdate(BaseModel):
    username: Optional[str]=Field(default=None,min_length=2,max_length=50)
    email: Optional[EmailStr]=None
    role: Optional[UserRole]=None

class ChangePassword(BaseModel):
    old_password: str = Field(min_length=8,max_length=25)
    new_password: str = Field(min_length=8,max_length=25)

# 返回给前端的模具（隐藏敏感信息）
class UserResponse(UserBase):
    id: int
    username:str
    role: str
    created_at: datetime
    # 核心配置：允许 Pydantic 直接从 SQLAlchemy 的数据库对象中提取属性
    model_config = {"from_attributes": True}



# 2. ItemTemplate 相关的 Schemas

class ItemTemplateBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    sku: str = Field(min_length=1, max_length=50)
    description: Optional[str] = None  # Optional 表示这个字段可以不传
    unit: Optional[str] = None

class ItemTemplateCreate(ItemTemplateBase):
    pass  # 创建时不需要额外的字段，直接继承 Base 即可

class ItemTemplateUpdate(BaseModel):
    name: Optional[str] = Field(default=None,min_length=1,max_length=100)
    sku: Optional[str] = Field(default=None,min_length=1,max_length=50)
    description: Optional[str] = None
    unit: Optional[str] = None

class ItemTemplateResponse(ItemTemplateBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# 3. schemas of inventory

class InventoryBase(BaseModel):
    template_id: int
    quantity: int
    
class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    template_id: Optional[int]=None
    quantity: Optional[int]=None

class InventoryResponse(InventoryBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes":True}

# 4. schemas of logs
    #inventory log
class InventoryLogBase(BaseModel):
    operation_type: str = Field(min_length=1,max_length=20)
    quantity_before: int
    quantity_after: int
    time_stamp: datetime

class InventoryLogResponse(InventoryLogBase):
    id: int
    model_config = {"from_attributes":True}

    #template log
class TemplateLogBase(BaseModel):
    operation_type: str = Field(min_length=1,max_length=20)
    time_stamp: datetime

class TemplateLogResponse(TemplateLogBase):
    id: int
    model_config = {"from_attributes":True}


