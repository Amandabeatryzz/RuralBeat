import sqlite3
from src.backend.config import DATABASE_PATH # Importa o caminho do banco de dados a partir do arquivo de configuração

def get_connection(): # Função para obter uma conexão com o banco de dados
    conn = sqlite3.connect(DATABASE_PATH) # Conecta ao banco de dados usando o caminho definido em DATABASE_PATH
    conn.row_factory = sqlite3.Row # Configura a conexão para retornar os resultados como dicionários, facilitando o acesso aos dados por nome de coluna
    return conn # Retorna a conexão estabelecida com o banco de dados para ser utilizada em outras partes do código, como nos serviços e controladores dos módulos.