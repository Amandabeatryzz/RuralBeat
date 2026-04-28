from src.backend.database.connection import get_connection

class DisciplinaRepository:

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM disciplinas")
        rows = cursor.fetchall()

        conn.close()
        return rows

    @staticmethod
    def create(codigo, nome, periodo, carga_horaria):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria)
            VALUES (?, ?, ?, ?)
        """, (codigo, nome, periodo, carga_horaria))

        conn.commit()
        disciplina_id = cursor.lastrowid

        conn.close()
        return disciplina_id
    
    @staticmethod
    def get_by_periodo(periodo):
      conn = get_connection()
      cursor = conn.cursor()

      cursor.execute(
        "SELECT * FROM disciplinas WHERE periodo = ?",
        (periodo,)
    )

      rows = cursor.fetchall()
      conn.close()
      return rows