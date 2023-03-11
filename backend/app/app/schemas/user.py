import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass
    # items: list[str] = []


class UserCreate(schemas.BaseUserCreate):
    pass

    # items: list[str] = []


class UserUpdate(schemas.BaseUserUpdate):
    pass
    # items: list[str] = []


# Additional properties to return via API
# class User(schemas.BaseUser[uuid.UUID]):
# pass
