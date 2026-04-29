from src.backend.database.connection import get_connection

class UserRepository:

    @staticmethod
    def create(nome, email, senha_hash):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )

        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        return user_id

    @staticmethod
    def get_by_email(email):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(       # Isso é uma consulta SQL para selecionar um usuário com base no email fornecido. O resultado é armazenado na variável user.
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
      # fetchone() é um método do cursor que retorna a próxima linha do resultado da consulta como um dicionário (ou None se não houver mais linhas). O resultado é armazenado na variável user.
        user = cursor.fetchone()
        conn.close()

        return user
    
    @staticmethod
    def existe_email(email):
      user = UserRepository.get_by_email(email)
      return user is not None