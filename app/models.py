from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from .database import Base
from app import types


class User(Base):

    __tablename__ = "user"  # It is a SQLAlchemy convention.

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="normal", nullable=False)  # admin, manager, nromal
    created_at = Column(DateTime,  server_default=func.now()) # lambda function to take real time


class ItemTemplate(Base):

    __tablename__ = "itemtemplate"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    sku = Column(String, unique=True, index=True)
    description = Column(String)
    unit = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class Inventory(Base): # item-in-inventory

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("itemtemplate.id"), index=True, nullable=False)
    quantity = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    item_template = relationship("ItemTemplate")


class OperationLog(Base):

    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    target_table = Column(String, nullable=False,index=True)
    target_id = Column(Integer, nullable=True,index=True)
    action = Column(
        SQLEnum(
            types.ActionType,
            values_callable=lambda x:[e.value for e in x]
        ),
        nullable=False,
        index=True )
    detail = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    user = relationship(User)