from datetime import datetime, timedelta # importações para manipulação de datas e horas
from typing import Optional # importação para indicar que um valor pode ser do tipo especificado ou None

from fastapi import Depends, HTTPException, status # importações do FastAPI para lidar com dependências, exceções HTTP  e status de resposta
from fastapi.security import OAuth2PasswordBearer  # importação para lidar com autenticação via OAuth2 usando senha
from jose import JWTError, jwt # importações para lidar com JSON Web Tokens (JWT) usando a biblioteca jose
from passlib.context import CryptContext # importação para lidar com hashing de senhas usando a biblioteca passlib

from config import settings
from database.connection import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")


# senha 

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# token
 # função para criar um token de acesso JWT, que inclui uma data de expiração e é assinado usando uma chave secreta e um algoritmo especificados nas configurações do aplicativo
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# dependências
# função para obter o usuário atual a partir do token de acesso fornecido, decodificando o token e buscando o usuário correspondente no banco de dados. Se o token for inválido ou expirado, ou se o usuário não for encontrado, uma exceção HTTP 401 é levantada.
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:# A função tenta decodificar o token usando a chave secreta e o algoritmo especificados. 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))# O ID do usuário é extraído do campo "sub" (subject) do payload do token. Se o campo "sub" estiver ausente ou não puder ser convertido para um inteiro, uma exceção de credenciais é levantada.
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
# Se a decodificação do token falhar por qualquer motivo (como um token inválido ou expirado), uma exceção de credenciais é levantada. Caso contrário, o ID do usuário é usado para buscar o usuário correspondente no banco de dados. Se o usuário não for encontrado, uma exceção de credenciais é levantada. Se tudo for bem-sucedido, o usuário é retornado como um dicionário.

    with get_db() as db:
        row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone() # busca o usuário no banco de dados usando o ID extraído do token
    if row is None: # Se o usuário não for encontrado, uma exceção de credenciais é levantada.
        raise credentials_exception 
    return dict(row)# Se o usuário for encontrado, ele é retornado como um dicionário.


def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("nivel", 0) < 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores")
    return current_user
# A função get_current_admin é uma dependência que verifica se o usuário atual tem um nível de acesso suficiente para ser considerado um administrador. Se o nível de acesso do usuário for menor que 2, uma exceção HTTP 403 é levantada indicando que o acesso é restrito a administradores. Caso contrário, o usuário atual é retornado.