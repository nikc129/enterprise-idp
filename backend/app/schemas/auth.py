from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "developer"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
