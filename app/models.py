from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from .database import Base
from app import types


class User(Base):

    __tablename__ = "users"  # It is a SQLAlchemy convention.

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="normal", nullable=False)  # admin, manager, nromal
    created_at = Column(DateTime,  default= lambda: datetime.now(timezone.utc)) # lambda function to take real time


class ItemTemplate(Base):

    __tablename__ = "itemtemplate"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    sku = Column(String, unique=True, index=True)
    description = Column(String)
    unit = Column(String)
    created_at = Column(DateTime, default= lambda: datetime.now(timezone.utc))

class Inventory(Base): # item-in-inventory

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("itemtemplate.id"), index=True, nullable=False)
    quantity = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, default= lambda: datetime.now(timezone.utc))
    item_template = relationship("ItemTemplate")


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), index=True, nullable=False)
    operation_type = Column(String, index=True, nullable=False)  # e.g., "create", "update", "delete"
    quantity_before = Column(Integer, nullable=False)
    quantity_after = Column(Integer, nullable=False)
    time_stamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships allow you to easily fetch the related objects in Python later
    operator = relationship("User")
    inventory = relationship("Inventory")


class TemplateLog(Base):
    __tablename__ = "template_logs"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    template_id = Column(Integer, ForeignKey("itemtemplate.id"), index=True, nullable=False)
    operation_type = Column(String, index=True, nullable=False)  # e.g., "create", "update", "delete"
    time_stamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    operator = relationship("User")
    item_template = relationship("ItemTemplate")