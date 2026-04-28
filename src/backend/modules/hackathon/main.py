from database import init_db
from backend.modules.hackathon.service import HackathonService

def menu():
    service = HackathonService()

    while True:
        print("\n--- HACKATHON RURALBEAT ---")
        print("1. Criar evento")
        print("2. Listar eventos")
        print("3. Criar equipe")
        print("4. Enviar projeto")
        print("5. Sair")

        op = input("Escolha: ")

        if op == "1":
            service.criar_evento()
        elif op == "2":
            service.listar_eventos()
        elif op == "3":
            service.criar_equipe()
        elif op == "4":
            service.criar_projeto()
        elif op == "5":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    init_db()
    menu()