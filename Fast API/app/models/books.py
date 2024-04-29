import datetime
from typing import TYPE_CHECKING

from tortoise import fields

from .base import Base

if TYPE_CHECKING:
    from .user import User

class Books(Base):
    """The Books model."""
    
    id: int = fields.IntField(pk=True)
    creator: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField('app.User', related_name='books')
    name: str = fields.CharField(max_length=200)
    created_at: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    description: str = fields.CharField(max_length=255)
    cover: str = fields.CharField(max_length=255, default="./img/book/covers/default.png")
    isAvailable: bool = fields.BooleanField(default=False)
    