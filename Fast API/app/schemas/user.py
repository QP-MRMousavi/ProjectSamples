from pydantic import BaseModel, Field, HttpUrl, EmailStr


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str
    avatar: HttpUrl | None


class UserUpdate(BaseModel):
    id: int | None = None
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    avatar: HttpUrl | None = None


class UserProfileUpdate(UserBase):
    id: int
    name: str | None
    avatar: HttpUrl | None


class UserPasswordUpdate(UserBase):
    id: int
    old_password: str
    new_password: str


class UserAuth(UserBase):
    email: EmailStr
    password: str


class DeleteUser(UserBase):
    id: int
    password: str
