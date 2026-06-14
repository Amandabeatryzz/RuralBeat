import sqlite3
from typing import Optional # para indicar que um campo é opcional, ou seja, pode ser omitido na requisição ou resposta. Isso é útil para campos que não são obrigatórios ou que podem ter valores nulos.


def list_all(db: sqlite3.Connection, tipo: Optional[str] = None) -> list: 
    query = "SELECT * FROM eventos"
    params = []
    if tipo:
        query += " WHERE tipo = ?"
        params.append(tipo)
    query += " ORDER BY data_evento"
    return [dict(r) for r in db.execute(query, params).fetchall()] 
# A função list_all retorna uma lista de eventos, opcionalmente filtrada por tipo (EVENTO ou HACKATHON). Ela constrói a consulta SQL dinamicamente com base na presença do parâmetro tipo e ordena os resultados pela data do evento.

def find_by_id(db: sqlite3.Connection, evento_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM eventos WHERE id = ?", (evento_id,)).fetchone()
    return dict(row) if row else None
# A função find_by_id busca um evento específico pelo seu ID. Se o evento for encontrado, ele é retornado como um dicionário; caso contrário, a função retorna None.

def create(db: sqlite3.Connection, data: dict) -> dict:
    cursor = db.execute(
        "INSERT INTO eventos (titulo, descricao, data_evento, local, tipo) VALUES (?,?,?,?,?)",
        (data["titulo"], data.get("descricao"), data.get("data_evento"), data.get("local"), data.get("tipo", "EVENTO")),
    )
    return find_by_id(db, cursor.lastrowid)
# A função create insere um novo evento no banco de dados usando os dados fornecidos em um dicionário. Ela retorna o evento recém-criado como um dicionário, incluindo o ID gerado pelo banco de dados.

def update(db: sqlite3.Connection, evento_id: int, fields: dict) -> Optional[dict]:
    if not fields:
        return find_by_id(db, evento_id)
    sets = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE eventos SET {sets} WHERE id = ?", list(fields.values()) + [evento_id])
    return find_by_id(db, evento_id)
#   A função update atualiza um evento existente com os campos fornecidos em um dicionário. Ela constrói dinamicamente a parte SET da consulta SQL com base nos campos presentes no dicionário e retorna o evento atualizado como um dicionário. Se nenhum campo for fornecido, ela simplesmente retorna o evento atual sem alterações.

def delete(db: sqlite3.Connection, evento_id: int) -> bool:
    return db.execute("DELETE FROM eventos WHERE id = ?", (evento_id,)).rowcount > 0


def inscricao_exists(db: sqlite3.Connection, user_id: int, evento_id: int) -> bool:
    return db.execute(
        "SELECT 1 FROM inscricoes_evento WHERE user_id = ? AND evento_id = ?", (user_id, evento_id)
    ).fetchone() is not None


def inscrever(db: sqlite3.Connection, user_id: int, evento_id: int) -> dict:
    cursor = db.execute(
        "INSERT INTO inscricoes_evento (user_id, evento_id) VALUES (?, ?)", (user_id, evento_id)
    )
    row = db.execute("SELECT * FROM inscricoes_evento WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return dict(row)


def cancelar_inscricao(db: sqlite3.Connection, user_id: int, evento_id: int) -> bool:
    return db.execute(
        "DELETE FROM inscricoes_evento WHERE user_id = ? AND evento_id = ?", (user_id, evento_id)
    ).rowcount > 0


def list_inscricoes_user(db: sqlite3.Connection, user_id: int) -> list:
    return [dict(r) for r in db.execute(
        "SELECT * FROM inscricoes_evento WHERE user_id = ?", (user_id,)
    ).fetchall()]