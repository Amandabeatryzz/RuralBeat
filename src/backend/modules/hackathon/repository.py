from database import get_connection

class HackathonRepository:

    def criar_evento(self, nome, tema):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO eventos (nome, tema) VALUES (?, ?)",
            (nome, tema)
        )
        conn.commit()
        conn.close()

    def listar_eventos(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM eventos")
        dados = cursor.fetchall()
        conn.close()
        return dados

    def criar_equipe(self, nome, evento_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO equipes (nome, evento_id) VALUES (?, ?)",
            (nome, evento_id)
        )
        conn.commit()
        conn.close()

    def criar_projeto(self, titulo, descricao, equipe_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projetos (titulo, descricao, equipe_id) VALUES (?, ?, ?)",
            (titulo, descricao, equipe_id)
        )
        conn.commit()
        conn.close()