# general types

import enum

class ActionType(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class TableName(enum.Enum):
    USER = "user"
    ITEM_TEMPLATE = "item_template"
    INVENTORY = "inventory"

class UserRole(enum.Enum):
    ADMIN = "admin"
    NORMAL = "normal"