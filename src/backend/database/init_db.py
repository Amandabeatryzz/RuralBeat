import sqlite3
import os # Importa o módulo os para lidar com caminhos de arquivos e diretórios
from src.backend.config import DATABASE_PATH # Importa o caminho do banco de dados a partir do arquivo de configuração

def init_db(): # Função para inicializar o banco de dados, criando as tabelas necessárias a partir dos scripts SQL
    conn = sqlite3.connect(DATABASE_PATH) # Conecta ao banco de dados usando o caminho definido em DATABASE_PATH
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # Define o diretório base do projeto para localizar os scripts SQL

    scripts = [
        os.path.join(BASE_DIR, "database", "schema.sql"), # Caminho para o script de criação do esquema do banco de dados
        os.path.join(BASE_DIR, "src/backend/database/migrations.sql"),
    ]

    for path in scripts:
      if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
                print(f" Executado: {path}")
        except Exception as e:
            print(f" Erro ao executar {path}: {e}")
      else:
        print(f" Arquivo não encontrado: {path}")

    conn.commit()
    conn.close()

    print("\n Banco inicializado com sucesso!")

if __name__ == "__main__":
    init_db()