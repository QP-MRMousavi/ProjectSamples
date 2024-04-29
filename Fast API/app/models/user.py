import datetime

from tortoise import fields

from .base import Base


class User(Base):
    """The User model."""

    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=200)
    created_at: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    email: str = fields.CharField(max_length=255)
    password: str = fields.CharField(max_length=255)
    avatar: str = fields.CharField(
        max_length=255, default="http:/localhost:3000/img/default.png"
    )
