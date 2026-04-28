from src.backend.modules.disciplinas.service import DisciplinaService


def listar():
    disciplinas = DisciplinaService.listar_disciplinas()

    if not disciplinas:
        print("\n⚠ Nenhuma disciplina cadastrada")
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
        print("❌ Entrada inválida")
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
        print("❌ Período inválido")
        return

    disciplinas = DisciplinaService.listar_por_periodo(periodo)

    if not disciplinas:
        print("⚠ Nenhuma disciplina encontrada para esse período")
        return

    print(f"\n--- DISCIPLINAS DO PERÍODO {periodo} ---")
    for d in disciplinas:
        print(f"{d['id']} | {d['codigo']} | {d['nome']} | {d['carga_horaria']}h")



def menu():
    while True:
        print("\n=== RURALBEAT  ===")
        print("1 - Listar disciplinas")
        print("2 - Criar disciplina")
        print("3 - Listar por período")
        print("4 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            listar()

        elif opcao == "2":
            criar()

        elif opcao == "3":
            listar_por_periodo()

        elif opcao == "4":
            print("Saindo...")
            break

        else:
            print("❌ Opção inválida")



if __name__ == "__main__":
    menu()