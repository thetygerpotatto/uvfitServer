from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class NameUpdateRequest(BaseModel):
    name: str

class UserDataUpdatateRequest(BaseModel):
    name: str | None
    age: int | None
    height: int | None
    weight:  int | None
    gender: str | None
    activity: str | None
    laydowntime: str | None
    isNew: bool | None

