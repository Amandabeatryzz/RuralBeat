from .repository import DisciplinaRepository

class DisciplinaService:

    @staticmethod
    def listar_disciplinas():
        disciplinas = DisciplinaRepository.get_all()

        return [
            {
                "id": d["id"],
                "codigo": d["codigo"],
                "nome": d["nome"],
                "periodo": d["periodo"],
                "carga_horaria": d["carga_horaria"]
            }
            for d in disciplinas
        ]

    @staticmethod
    def listar_por_periodo(periodo):
        disciplinas = DisciplinaRepository.get_by_periodo(periodo)

        return [
            {
                "id": d["id"],
                "codigo": d["codigo"],
                "nome": d["nome"],
                "periodo": d["periodo"],
                "carga_horaria": d["carga_horaria"]
            }
            for d in disciplinas
        ]

    @staticmethod
    def criar_disciplina(data):
        disciplina_id = DisciplinaRepository.create(
            data["codigo"],
            data["nome"],
            data["periodo"],
            data["carga_horaria"]
        )

        return {"id": disciplina_id}