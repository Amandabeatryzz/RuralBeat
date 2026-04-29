import bcrypt
from .user_repository import UserRepository

class UserService:

    @staticmethod
    def cadastrar(data):
        existing = UserRepository.get_by_email(data["email"])

        if existing:
            return {"error": "Usuário já existe"}

        senha_hash = bcrypt.hashpw(
            data["senha"].encode(),
            bcrypt.gensalt()
        )

        user_id = UserRepository.create(
            data["nome"],
            data["email"],
            senha_hash
        )

        return {"id": user_id}

     
    @staticmethod
    def login(email, senha):
        user = UserRepository.get_by_email(email)

        if not user:
            return {"error": "Usuário não encontrado"}

        if not bcrypt.checkpw(
            senha.encode(),
            user["senha"]
        ):
            return {"error": "Senha incorreta"}

        return {
            "id": user["id"],
            "nome": user["nome"],
            "email": user["email"]
        }
        
    @staticmethod
    def existe_email(email):
     user = UserRepository.get_by_email(email)
     return user is not None