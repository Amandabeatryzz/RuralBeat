from pydantic import BaseModel, EmailStr # para criar modelos de dados que serão usados para validar e serializar as requisições e respostas da API. O BaseModel é a classe base do Pydantic, que é uma biblioteca de validação de dados usada pelo FastAPI para garantir que os dados recebidos e enviados pela API estejam no formato correto. O EmailStr é um tipo específico do Pydantic que valida se o valor é um endereço de email válido.
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
    token_type: str = "bearer" # O campo token_type é definido como "bearer" por padrão, indicando que o token de acesso é do tipo Bearer, que é um tipo comum de token usado para autenticação em APIs. O campo access_token contém o token real que será usado para autenticar as requisições subsequentes.
    user: UserOut