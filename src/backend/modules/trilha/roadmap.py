import sqlite3
from collections import defaultdict

DB = "ruralbeat.db"

def conectar():
    return sqlite3.connect(DB)


# =============================
# CARREGAR DADOS DO BANCO
# =============================
def carregar_disciplinas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, codigo, nome, periodo FROM disciplinas")
    disciplinas = cursor.fetchall()

    conn.close()

    return {str(d[0]): {
        "codigo": d[1],
        "nome": d[2],
        "periodo": d[3]
    } for d in disciplinas}


def carregar_prerequisitos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT disciplina_id, requisito_id FROM pre_requisitos")
    dados = cursor.fetchall()

    conn.close()

    grafo = defaultdict(list)

    for disciplina, requisito in dados:
        grafo[str(disciplina)].append(str(requisito))

    return grafo



def disciplinas_liberadas(disciplinas, grafo, concluidas):
    liberadas = []

    for d_id in disciplinas:
        requisitos = grafo.get(d_id, [])

        if all(r in concluidas for r in requisitos):
            if d_id not in concluidas:
                liberadas.append(d_id)

    return liberadas


def mostrar_trilha(disciplinas, grafo, concluidas):
    print("\n=== TRILHA BSI (RuralBeat) ===\n")

    # agrupar por período
    periodos = defaultdict(list)
    for d_id, d in disciplinas.items():
        periodos[d["periodo"]].append((d_id, d))

    for periodo in sorted(periodos.keys()):
        print(f"\n📚 PERÍODO {periodo}")
        print("-" * 30)

        for d_id, d in periodos[periodo]:
            if d_id in concluidas:
                status = "🟢 CONCLUÍDA"
            elif all(r in concluidas for r in grafo.get(d_id, [])):
                status = "🟡 LIBERADA"
            else:
                status = "🔒 BLOQUEADA"

            print(f"{d['codigo']} - {d['nome']} [{status}]")

            # mostrar requisitos
            if grafo.get(d_id):
                print("   ↳ Requisitos:", [
                    disciplinas[r]["codigo"] for r in grafo[d_id]
                ])

    print("\n")

def main():
    disciplinas = carregar_disciplinas()
    grafo = carregar_prerequisitos()

    # simulação: usuário já concluiu essas disciplinas
    concluidas = set()

    while True:
        mostrar_trilha(disciplinas, grafo, concluidas)

        print("Digite o CÓDIGO da disciplina concluída (ou 'sair'):")
        entrada = input("> ").strip()

        if entrada.lower() == "sair":
            break

        # buscar disciplina pelo código
        encontrada = None
        for d_id, d in disciplinas.items():
            if d["codigo"] == entrada:
                encontrada = d_id
                break

        if not encontrada:
            print("❌ Disciplina não encontrada\n")
            continue

        concluidas.add(encontrada)
        print("✅ Marcada como concluída!\n")


if __name__ == "__main__":
    main()