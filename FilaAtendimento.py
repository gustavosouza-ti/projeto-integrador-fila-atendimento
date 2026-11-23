# ==============================================================================
# PROJETO INTEGRADOR: LABORATÓRIO DE PROGRAMAÇÃO (UNISA - ADS)
# Tema: Sistema de Fila de Atendimento com Prioridade e Histórico de Desfazer
# Recursos utilizados: variáveis, tipos primitivos, operadores, if/elif/else,
# while, for, range, listas, tuplas, dicionários e funções (def/return).
# ==============================================================================

# Tupla imutável com os tipos de atendimento permitidos
CATEGORIAS_VALIDAS = ("NORMAL", "PRIORITARIO")


def formatar_codigo(prefixo, numero):
    """Gera o código da senha no padrão N001 ou P001 usando lógica básica."""
    if numero < 10:
        return prefixo + "00" + str(numero)
    elif numero < 100:
        return prefixo + "0" + str(numero)
    else:
        return prefixo + str(numero)


def gerar_senha(fila_normal, fila_prioritaria, nome, categoria, motivo, contadores):
    """Cria um dicionário representando a senha e adiciona na fila correspondente."""
    nome_limpo = nome.strip()
    categoria_limpa = categoria.strip().upper()
    motivo_limpo = motivo.strip()

    if nome_limpo == "" or motivo_limpo == "":
        return False, "Erro: nome e motivo do atendimento são obrigatórios."

    if categoria_limpa not in CATEGORIAS_VALIDAS:
        return False, "Erro: categoria inválida. Use NORMAL ou PRIORITARIO."

    if categoria_limpa == "PRIORITARIO":
        contadores["prioritario"] = contadores["prioritario"] + 1
        codigo = formatar_codigo("P", contadores["prioritario"])
        senha = {
            "codigo": codigo,
            "nome": nome_limpo,
            "categoria": categoria_limpa,
            "motivo": motivo_limpo
        }
        fila_prioritaria.append(senha)
    else:
        contadores["normal"] = contadores["normal"] + 1
        codigo = formatar_codigo("N", contadores["normal"])
        senha = {
            "codigo": codigo,
            "nome": nome_limpo,
            "categoria": categoria_limpa,
            "motivo": motivo_limpo
        }
        fila_normal.append(senha)

    return True, "Senha " + codigo + " gerada para " + nome_limpo + " (" + categoria_limpa + ")."


def chamar_proximo(fila_normal, fila_prioritaria, historico_atendidos):
    """Chama o próximo da fila (prioridade primeiro) e empilha no histórico."""
    if len(fila_prioritaria) > 0:
        proximo = fila_prioritaria.pop(0)
        historico_atendidos.append(proximo)
        return True, proximo
    elif len(fila_normal) > 0:
        proximo = fila_normal.pop(0)
        historico_atendidos.append(proximo)
        return True, proximo
    else:
        return False, None


def desfazer_ultimo_atendimento(fila_normal, fila_prioritaria, historico_atendidos):
    """Remove o último atendimento do histórico (pilha) e devolve ao início da fila."""
    if len(historico_atendidos) == 0:
        return False, "Nenhum atendimento registrado no histórico para desfazer."

    ultimo = historico_atendidos.pop()
    if ultimo["categoria"] == "PRIORITARIO":
        fila_prioritaria.insert(0, ultimo)
    else:
        fila_normal.insert(0, ultimo)

    return True, "Atendimento da senha " + ultimo["codigo"] + " (" + ultimo["nome"] + ") foi desfeito."


def buscar_senha(fila_normal, fila_prioritaria, historico_atendidos, codigo_busca):
    """Procura uma senha nas filas de espera ou no histórico usando laço for."""
    alvo = codigo_busca.strip().upper()

    for i in range(len(fila_prioritaria)):
        if fila_prioritaria[i]["codigo"] == alvo:
            return "Aguardando na fila PRIORITÁRIA (posição " + str(i + 1) + "): " + fila_prioritaria[i]["nome"]

    for i in range(len(fila_normal)):
        if fila_normal[i]["codigo"] == alvo:
            return "Aguardando na fila NORMAL (posição " + str(i + 1) + "): " + fila_normal[i]["nome"]

    for item in historico_atendidos:
        if item["codigo"] == alvo:
            return "Já atendido(a): " + item["nome"] + " (" + item["categoria"] + ")"

    return "Senha não encontrada no sistema."


def gerar_resumo(fila_normal, fila_prioritaria, historico_atendidos):
    """Retorna um dicionário com os totais atuais do atendimento."""
    atendidos_prioritarios = 0
    atendidos_normais = 0

    for item in historico_atendidos:
        if item["categoria"] == "PRIORITARIO":
            atendidos_prioritarios = atendidos_prioritarios + 1
        else:
            atendidos_normais = atendidos_normais + 1

    resumo = {
        "aguardando_prioritario": len(fila_prioritaria),
        "aguardando_normal": len(fila_normal),
        "total_aguardando": len(fila_prioritaria) + len(fila_normal),
        "atendidos_prioritario": atendidos_prioritarios,
        "atendidos_normal": atendidos_normais,
        "total_atendidos": len(historico_atendidos)
    }
    return resumo


def exibir_menu():
    print("\n==============================================")
    print("   SISTEMA DE FILA DE ATENDIMENTO - UNISA     ")
    print("==============================================")
    print("1 - Emitir nova senha (Normal ou Prioritário)")
    print("2 - Chamar próximo atendimento")
    print("3 - Desfazer último atendimento (Histórico)")
    print("4 - Visualizar filas de espera")
    print("5 - Consultar status de uma senha")
    print("6 - Exibir resumo gerencial e histórico")
    print("0 - Encerrar sistema")


def executar_sistema():
    fila_normal = []
    fila_prioritaria = []
    historico_atendidos = []
    contadores = {"normal": 0, "prioritario": 0}

    # Carga inicial de exemplo para facilitar os testes
    gerar_senha(fila_normal, fila_prioritaria, "Carlos Silva", "NORMAL", "Entrega de documentos", contadores)
    gerar_senha(fila_normal, fila_prioritaria, "Maria Oliveira", "PRIORITARIO", "Atendimento preferencial", contadores)
    gerar_senha(fila_normal, fila_prioritaria, "João Santos", "NORMAL", "Consulta cadastral", contadores)

    executando = True
    while executando:
        exibir_menu()
        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            nome = input("Nome do cliente/solicitante: ")
            categoria = input("Categoria (NORMAL ou PRIORITARIO): ")
            motivo = input("Motivo do atendimento: ")
            sucesso, mensagem = gerar_senha(fila_normal, fila_prioritaria, nome, categoria, motivo, contadores)
            print(mensagem)

        elif opcao == "2":
            chamou, senha_chamada = chamar_proximo(fila_normal, fila_prioritaria, historico_atendidos)
            if chamou:
                print("\n>>> CHAMANDO SENHA:", senha_chamada["codigo"], "-", senha_chamada["nome"],
                      "[" + senha_chamada["categoria"] + "] | Motivo:", senha_chamada["motivo"])
            else:
                print("\nNão há senhas aguardando nas filas no momento.")

        elif opcao == "3":
            desfez, mensagem = desfazer_ultimo_atendimento(fila_normal, fila_prioritaria, historico_atendidos)
            print("\n" + mensagem)

        elif opcao == "4":
            print("\n--- FILA PRIORITÁRIA ---")
            if len(fila_prioritaria) == 0:
                print("Vazia.")
            else:
                for pos in range(len(fila_prioritaria)):
                    item = fila_prioritaria[pos]
                    print(str(pos + 1) + "º -", item["codigo"], "|", item["nome"], "|", item["motivo"])

            print("\n--- FILA NORMAL ---")
            if len(fila_normal) == 0:
                print("Vazia.")
            else:
                for pos in range(len(fila_normal)):
                    item = fila_normal[pos]
                    print(str(pos + 1) + "º -", item["codigo"], "|", item["nome"], "|", item["motivo"])

        elif opcao == "5":
            codigo_busca = input("Informe o código da senha (ex: P001 ou N001): ")
            resultado = buscar_senha(fila_normal, fila_prioritaria, historico_atendidos, codigo_busca)
            print("\nResultado:", resultado)

        elif opcao == "6":
            resumo = gerar_resumo(fila_normal, fila_prioritaria, historico_atendidos)
            print("\n--- RESUMO GERENCIAL ---")
            for chave in resumo:
                print(chave, "->", resumo[chave])

            print("\n--- HISTÓRICO DE ATENDIMENTOS CONCLUÍDOS ---")
            if len(historico_atendidos) == 0:
                print("Nenhum atendimento concluído até o momento.")
            else:
                for reg in historico_atendidos:
                    print(reg["codigo"], "|", reg["nome"], "|", reg["categoria"], "|", reg["motivo"])

        elif opcao == "0":
            print("\nEncerrando o sistema de atendimento. Até logo!")
            executando = False

        else:
            print("\nOpção inválida! Escolha um número de 0 a 6.")


if __name__ == "__main__":
    executar_sistema()