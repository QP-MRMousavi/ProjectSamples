import random
import string

from app.schemas import UserCreate


def new_random_user() -> UserCreate:
    return UserCreate(
        name=random_letters(),
        email=f"{random_letters()}@gmail.com",
        password=random_letters(),
        avatar=f"http://localhost:3000/img/avatars/{random_letters()}.png",
    )


def get_specific_user() -> UserCreate:
    return UserCreate(
        name="SPECIFIC USER",
        email="SPECIFICUSER@gmail.com",
        password="IT MUST BE RANDOM HASH",
        avatar=f"http://localhost:3000/img/avatars/SPECIFIC-USER.png",
    )


def new_id():
    return (random.randint(1_000_000, 2_000_000),)
