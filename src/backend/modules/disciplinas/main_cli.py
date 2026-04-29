from src.backend.modules.disciplinas.service import DisciplinaService
from src.backend.modules.usuario.user_service import UserService
import re



def validar_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) # Expressão regular para validar formato de email



def validar_senha(senha):
    if len(senha) < 6:
        return False
    if not any(c.isdigit() for c in senha):
        return False
    if not any(c.isalpha() for c in senha):
        return False
    return True

def listar():
    disciplinas = DisciplinaService.listar_disciplinas()

    if not disciplinas:
        print("\n Nenhuma disciplina cadastrada")
        return

    print("\n--- TODAS AS DISCIPLINAS ---")
    for d in disciplinas:
        print(f"{d['id']} | {d['codigo']} | {d['nome']} | P{d['periodo']} | {d['carga_horaria']}h")


def criar():
    print("\n--- NOVA DISCIPLINA ---")

    try:
        codigo = input("Código: ").strip()
        nome = input("Nome: ").strip()
        periodo = int(input("Período (1-10): "))
        carga = int(input("Carga horária: "))
    except ValueError:
        print(" Entrada inválida")
        return

    result = DisciplinaService.criar_disciplina({
        "codigo": codigo,
        "nome": nome,
        "periodo": periodo,
        "carga_horaria": carga
    })

    print(f"✔ Disciplina criada com ID {result['id']}")


def listar_por_periodo():
    try:
        periodo = int(input("Digite o período (1-10): "))
    except ValueError:
        print(" Período inválido")
        return

    disciplinas = DisciplinaService.listar_por_periodo(periodo)

    if not disciplinas:
        print(" Nenhuma disciplina encontrada para esse período")
        return

    print(f"\n--- DISCIPLINAS DO PERÍODO {periodo} ---")
    for d in disciplinas:
        print(f"{d['id']} | {d['codigo']} | {d['nome']} | {d['carga_horaria']}h")


def autenticar():
    while True:
        print("\n=== LOGIN ===")
        print("1 - Login")
        print("2 - Cadastrar")
        print("3 - Sair")

        opcao = input("Escolha: ").strip()

        # LOGIN
        if opcao == "1":
            email = input("Email: ")

            if not validar_email(email):
                print(" Email inválido")
                continue

            email = email.strip().lower()
            senha = input("Senha: ")

            user = UserService.login(email, senha)

            if "error" in user:
                print(user["error"])
            else:
                print(f"\n Bem-vindo, {user['nome']}!")
                return user

        # CADASTRO
        elif opcao == "2":
            nome = input("Nome: ")
            email = input("Email: ")

            if not validar_email(email):
                print(" Email inválido (ex: nome@email.com)")
                continue

            # normalizar email
            email = email.strip().lower()

            # bloquear duplicado
            if UserService.existe_email(email):
                print(" Email já cadastrado")
                continue

            senha = input("Senha: ")

            
            if not validar_senha(senha):
                print(" Senha deve ter pelo menos 6 caracteres, com letras e números")
                continue

            result = UserService.cadastrar({
                "nome": nome,
                "email": email,
                "senha": senha
            })

            if "error" in result:
                print(result["error"])
            else:
                print(" Usuário cadastrado!")

        # SAIR
        elif opcao == "3":
            return None

        # OPÇÃO INVÁLIDA
        else:
            print(" Opção inválida")

def menu(user):
    while True:
        print(f"\n=== RURALBEAT | Usuário: {user['nome']} ===")
        print("1 - Listar disciplinas")
        print("2 - Criar disciplina")
        print("3 - Listar por período")
        print("4 - Logout")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            listar()

        elif opcao == "2":
            criar()

        elif opcao == "3":
            listar_por_periodo()

        elif opcao == "4":
            print(" Logout realizado")
            break

        else:
            print(" Opção inválida")


if __name__ == "__main__":
    while True:
        user = autenticar()

        if not user:
            print("Encerrando sistema...")
            break

        menu(user)