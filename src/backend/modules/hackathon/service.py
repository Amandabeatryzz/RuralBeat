from repository import HackathonRepository

class HackathonService:

    def __init__(self):
        self.repo = HackathonRepository()

    def criar_evento(self):
        nome = input("Nome do evento: ")
        tema = input("Tema: ")
        self.repo.criar_evento(nome, tema)
        print("Evento criado!")

    def listar_eventos(self):
        eventos = self.repo.listar_eventos()
        for e in eventos:
            print(f"ID: {e[0]} | Nome: {e[1]} | Tema: {e[2]}")

    def criar_equipe(self):
        nome = input("Nome da equipe: ")
        evento_id = input("ID do evento: ")
        self.repo.criar_equipe(nome, evento_id)
        print("Equipe criada!")

    def criar_projeto(self):
        titulo = input("Título do projeto: ")
        descricao = input("Descrição: ")
        equipe_id = input("ID da equipe: ")
        self.repo.criar_projeto(titulo, descricao, equipe_id)
        print("Projeto enviado!")