from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    id: int
    nome: str
    email: str
    nivel: int


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut