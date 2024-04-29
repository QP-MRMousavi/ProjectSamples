from typing import Any

from tortoise import models


class Base(models.Model):
    """The Base model."""

    id: Any

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {str(self.__dict__)}>"
