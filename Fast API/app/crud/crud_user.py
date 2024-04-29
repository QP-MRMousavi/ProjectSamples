from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.queryset import QuerySet

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_user_by_email_and_password(
        self, db: BaseDBAsyncClient, obj_data: UserCreate
    ) -> User | None:
        return (
            await self.model.filter(password=obj_data.password, email=obj_data.email)
            .using_db(db)
            .first()
        )

    async def get_user_by_id_or_email(
        self, db: BaseDBAsyncClient, obj_data: UserUpdate
    ) -> User | None:
        selector_dict = obj_data.dict(exclude_unset=True)
        if len(selector_dict) != 1:
            raise ValueError("obj_in does not contain single update")

        return await self.model.filter(email=obj_data.email).using_db(db).first()

    async def create_user(
        self, db: BaseDBAsyncClient, obj_data: UserCreate
    ) -> tuple[User | None, bool]:
        user = await self.get_user_by_id_or_email(
            db, obj_data=UserUpdate(email=obj_data.email)
        )
        if user is not None:
            return None, False
        return await self.create(db, obj_in=obj_data), True

    async def update_user(
        self,
        db: BaseDBAsyncClient,
        *,
        db_obj: User,
        obj_in: UserUpdate,
    ) -> tuple[User, bool]:
        single_update_dict = obj_in.dict(exclude_unset=True)
        if len(single_update_dict) != 1:
            raise ValueError("obj_in does not contain single update")
        id_list: list[int] = (
            await self.model.filter(**single_update_dict)  # type: ignore
            .using_db(db)
            .values_list("id", flat=True)
        )
        if id_list and db_obj.id not in id_list:
            return db_obj, False
        return await self.update_changes_only(db, db_obj=db_obj, obj_in=obj_in), True

    async def delete_user_by_id(
        self, db: BaseDBAsyncClient, obj_data: UserUpdate
    ) -> bool:
        return (await self.delete_by_id(db, record_id=obj_data.id)) == 1


user = CRUDUser()
