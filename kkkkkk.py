class MatrizCurricular:
    
    def __init__(self) -> None:
        self.TRILHAS: dict[str, list[str]] = {
            "backend_engenharia": [
                "Princípios de Programação",
                "Fundamentos de Problemas Computacionais I",
                "Fundamentos de Problemas Computacionais II",
                "Paradigmas de Programação",
                "Desenvolvimento de Sistemas de Informação",
                "Infraestrutura de Software"
            ],
            "dados_e_ia": [
                "Introdução ao Armazenamento e Análise de Dados",
                "Modelagem de Dados",
                "Estatística Aplicada à Análise de Dados",
                "Sistemas de Apoio à Decisão",
                "Tópicos Avançados em Inteligência Artificial"
            ],
            "seguranca_e_redes": [
                "Elementos de Sistemas Computacionais",
                "Princípios de Software Básico",
                "Segurança e Auditoria de Sistemas",
                "Fundamentos de Criptografia",
                "Tópicos Avançados em Redes de Computadores I"
            ],
            "gestao_e_negocios": [
                "Introdução à Administração",
                "Empreendedorismo e Inovação",
                "Fundamentos de Estratégia Competitiva",
                "Gestão do Conhecimento",
                "Inovação em TIC"
            ]
        }

        self.PRE_REQUISITOS: dict[str, list[str]] = {
            "Fundamentos de Problemas Computacionais I": ["Princípios de Programação"],
            "Fundamentos de Problemas Computacionais II": ["Fundamentos de Problemas Computacionais I"],
            "Paradigmas de Programação": ["Princípios de Programação"],
            "Desenvolvimento de Sistemas de Informação": ["Princípios de Programação"],
            "Infraestrutura de Software": ["Desenvolvimento de Sistemas de Informação"],
            "Modelagem de Dados": ["Introdução ao Armazenamento e Análise de Dados"],
            "Estatística Aplicada à Análise de Dados": ["Fundamentos Matemáticos para Sistemas de Informação II"],
            "Sistemas de Apoio à Decisão": ["Modelagem de Dados", "Estatística Aplicada à Análise de Dados"],
            "Tópicos Avançados em Inteligência Artificial": ["Estatística Aplicada à Análise de Dados", "Paradigmas de Programação"],
            "Segurança e Auditoria de Sistemas": ["Elementos de Sistemas Computacionais"],
            "Fundamentos de Criptografia": ["Fundamentos Matemáticos para Sistemas de Informação II"],
            "Tópicos Avançados em Redes de Computadores I": ["Elementos de Sistemas Computacionais"],
            "Empreendedorismo e Inovação": ["Introdução à Administração"],
            "Fundamentos de Estratégia Competitiva": ["Introdução à Administração"],
            "Gestão do Conhecimento": ["Fundamentos de Sistemas de Informação II"]
        }
        
        self.PERIODO_RESTRICAO: int = 3
        self.TRILHAS_RESTRITAS: dict[str] = ["backend_engenharia", "dados_e_ia", "seguranca_e_redes"]

    def validar_restricao_periodo(self, periodo: int, trilha: str) -> bool:
        """Regra de negócio: Alunos do 3º período não podem fazer algumas trilhas(restrição pedida)."""
        if periodo == self.PERIODO_RESTRICAO and trilha in self.TRILHAS_RESTRITAS:
            return False
        return True

    def obter_requisitos(self, disciplina: str) -> list[str]:
        """Retorna a lista de pré-requisitos de uma disciplina."""
        return self.PRE_REQUISITOS.get(disciplina, [])

    def formatar_nome_trilha(self, chave_trilha: str) -> str:
        return chave_trilha.replace("_", " ").title().replace(" E ", " e ")
   
class Aluno:
    def __init__(self, periodo: int, trilha: str) -> None:
        self.periodo: int = periodo
        self.trilha: str = trilha
        self.disciplinas_escolhidas: list[str] = []
        """ Histórico fixo  (cadeiras passadas concluídas, pode-se futuramente criar uma classe chamada progresso)"""
        self.historico: list[str] = [
            "Fundamentos Matemáticos para Sistemas de Informação II",
            "Fundamentos de Sistemas de Informação II" ]
        self.MAX_DISCIPLINAS: int = 4

    def tem_vagas(self) -> bool:
        return len(self.disciplinas_escolhidas) < self.MAX_DISCIPLINAS

    def ja_matriculado(self, disciplina: str) -> bool:
        """Verifica se a disciplina já está na lista de escolhas atual."""
        return disciplina in self.disciplinas_escolhidas

    def possui_requisito(self, requisito: str) -> bool:
        """Verifica se o aluno atende a um requisito (via histórico ou escolha atual)."""
        return requisito in self.historico 

    def adicionar_disciplina(self, disciplina: str) -> None:
        """Adiciona a disciplina."""
        self.disciplinas_escolhidas.append(disciplina)


class SistemaMatricula:
    def __init__(self) -> None:
        self.matriz = MatrizCurricular()
        self.aluno: Aluno | None = None

    def obter_inteiro_seguro(self, mensagem: str) -> int:
        """exceção para impedir quebra por inputs de texto inválidos."""
        while True:
            try:
                valor = int(input(mensagem))
                if valor >= 0:
                    return valor
                print("[ERRO] Digite um número positivo.")
            except ValueError:
                print("[ERRO] Entrada inválida. Digite apenas números inteiros.")

    def configurar_aluno(self) -> Aluno:
        chaves_trilhas = list(self.matriz.TRILHAS.keys())
        
        while True:
            periodo = self.obter_inteiro_seguro("\nDigite seu período atual (ex: 1, 2, 3...): ")
            
            print("\n===== TRILHAS DISPONÍVEIS =====")
            for i, chave in enumerate(chaves_trilhas, start=1):
                print(f"{i} - {self.matriz.formatar_nome_trilha(chave)}")
                
            opcao_trilha = self.obter_inteiro_seguro("\nDigite o número da sua trilha: ")
            
            if 1 <= opcao_trilha <= len(chaves_trilhas):
                trilha_escolhida = chaves_trilhas[opcao_trilha - 1]
                
                # Validação usando as regras da Matriz Curricular
                if self.matriz.validar_restricao_periodo(periodo, trilha_escolhida):
                    print(f"\n[SUCESSO] Acesso liberado para a trilha escolhida!")
                    return Aluno(periodo, trilha_escolhida)
                
                print(f"\n[BLOQUEADO] Alunos do {self.matriz.PERIODO_RESTRICAO}º período não podem")
                print(f"cursar a trilha de {self.matriz.formatar_nome_trilha(trilha_escolhida)}.")
                print("Tente novamente ajustando as informações.")
                print("-" * 55)
            else:
                print("[ERRO] Opção de trilha inválida. Recomeçando configuração...")

    def menu_selecao_disciplinas(self) -> str | None:
        """Exibe as disciplinas filtradas e gerencia o input da escolha."""
        disciplinas_da_trilha = self.matriz.TRILHAS[self.aluno.trilha]
        trilha_nome = self.matriz.formatar_nome_trilha(self.aluno.trilha)
        
        print(f"\n===== DISCIPLINAS ({trilha_nome}) =====")
        for i, disc in enumerate(disciplinas_da_trilha, start=1):
            status = "[Selecionada]" if self.aluno.ja_matriculado(disc) else ""
            print(f"{i} - {disc} {status}")
        print("0 - [Finalizar/Sair]")
        
        opcao = self.obter_inteiro_seguro("\nDigite o NÚMERO da disciplina desejada: ")
        
        if opcao == 0:
            return "SAIR"
        if 1 <= opcao <= len(disciplinas_da_trilha):
            return disciplinas_da_trilha[opcao - 1]
            
        print("[ERRO] Código inválido.")
        return None

    def executar(self) -> None:
        print("====================================================")
        print("                SISTEMA DE MATRÍCULA                ")
        print("====================================================")
        
        self.aluno = self.configurar_aluno()
        print(f"Você pode escolher até {self.aluno.MAX_DISCIPLINAS} disciplinas.")

        # Loop de Matrícula nas Disciplinas
        while self.aluno.tem_vagas():
            print(f"\nProgresso: {len(self.aluno.disciplinas_escolhidas)}/{self.aluno.MAX_DISCIPLINAS}")
            
            disciplina = self.menu_selecao_disciplinas()
            
            if disciplina == "SAIR":
                break
            if not disciplina:
                continue

            # Validação 1: Já adicionada? (Estado interno do Aluno)
            if self.aluno.ja_matriculado(disciplina):
                print(f"[AVISO] Você já selecionou '{disciplina}'.")
                continue

            # Validação 2: Pré-requisitos? (Matriz valida cruzando dados com o Aluno)
            requisitos = self.matriz.obter_requisitos(disciplina)
            requisitos_atendidos = True
            
            for req in requisitos:
                if not self.aluno.possui_requisito(req):
                    print(f"[BLOQUEIO] Falta o pré-requisito: '{req}'")
                    requisitos_atendidos = False
                    break
            
            if not requisitos_atendidos:
                continue

            # passou por todas as validações, pode adicionar
            self.aluno.adicionar_disciplina(disciplina)
            print(f"[OK] '{disciplina}' vinculada com sucesso!")

        # Emissão do Relatório Final
        self.exibir_recibo()

    def exibir_recibo(self) -> None:
        print("\n====================================================")
        print("               MATRÍCULA FINALIZADA                 ")
        print("====================================================")
        print(f"Trilha: {self.matriz.formatar_nome_trilha(self.aluno.trilha)}")
        print(f"Período Informado: {self.aluno.periodo}º")
        print("Disciplinas confirmadas para o próximo semestre:")
        
        if not self.aluno.disciplinas_escolhidas:
            print("  [Nenhuma disciplina selecionada]")
        else:
            for d in self.aluno.disciplinas_escolhidas:
                print(f"  - {d}")
        print("====================================================")


# ---------------------------------------------------------------------
# EXECUÇÃO DO PROGRAMA
# ---------------------------------------------------------------------
if __name__ == "__main__":
    sistema = SistemaMatricula()
    sistema.executar()
    
    