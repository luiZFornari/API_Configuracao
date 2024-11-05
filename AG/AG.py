import random
import copy

def selecionar_pais(populacao, componentes, peso_pontuacoes):
    pais = []
    for _ in range(len(populacao)):
        concorrentes = random.sample(populacao, min(3, len(populacao)))
        pais.append(max(concorrentes, key=lambda x: calcular_pontuacao_total(x, componentes, peso_pontuacoes)))
    return pais

def criar_configuracao_aleatoria(componentes, limite_valor):
    configuracao = {}
    for tipo, opcoes in componentes.items():
        opcoes_abaixo_do_limite = [comp for comp in opcoes if "price" in opcoes[comp] and opcoes[comp]["price"] <= limite_valor]
        if opcoes_abaixo_do_limite:
            componente_escolhido = random.choice(opcoes_abaixo_do_limite)
            configuracao[tipo] = componente_escolhido
    return configuracao

def calcular_custo_total(configuracao, componentes):
    custo_total = 0
    for tipo, escolha in configuracao.items():
        componente = componentes.get(tipo, {}).get(escolha)
        custo_total += componente.get('price', 0)
    return custo_total

def calcular_pontuacao_total(configuracao, componentes, peso_pontuacoes):
    pontuacao_total = 0
    for tipo, escolha in configuracao.items():
        score = componentes[tipo][escolha]["score"]
        peso = peso_pontuacoes.get(tipo)
        score_normalizado = (score - min(componentes[tipo][opcao]["score"] for opcao in componentes[tipo])) / \
                            (max(componentes[tipo][opcao]["score"] for opcao in componentes[tipo]) - \
                             min(componentes[tipo][opcao]["score"] for opcao in componentes[tipo]))
        pontuacao_total += score_normalizado * peso
    return pontuacao_total

def crossover(configuracao1, configuracao2):
    nova_configuracao = {}
    ponto_crossover = random.choice(list(configuracao1.keys()))
    for tipo in configuracao1:
        # Alteração para que a escolha seja aleatória entre os pais
        escolha = configuracao1[tipo] if random.random() < 0.5 else configuracao2[tipo]
        nova_configuracao[tipo] = escolha
    return nova_configuracao

def mutacao(configuracao, componentes, taxa_mutacao):
    tipo_mutacao = random.choice(list(configuracao.keys()))
    escolha_mutacao = random.choice(list(componentes[tipo_mutacao].keys()))

    if random.random() < taxa_mutacao:
        configuracao[tipo_mutacao] = escolha_mutacao
    return configuracao

def algoritmo_genetico(componentes, limite_valor,  geracoes=5000, tamanho_populacao=5000, taxa_mutacao=0.9):
    populacao = []
    peso_pontuacoes = {
        "placa_mae": 1.0,
        "processador": 2.0,
        "memoria_ram": 1.0,
        "placa_de_video": 2.0,
        "fonte": 0.5,
        "resfriamento": 0.5,
        "armazenamento": 1.0,
    }
    while not populacao:
        populacao = [criar_configuracao_aleatoria(componentes, limite_valor) for _ in range(tamanho_populacao)]

    melhor_config = {}
    custo_melhor_config = float('inf')
    pontuacao_melhor_config = float('-inf')

    for geracao in range(geracoes):
        populacao = sorted(populacao, key=lambda x: calcular_custo_total(x, componentes))

        pais = selecionar_pais(populacao, componentes, peso_pontuacoes)
        proxima_geracao = []

        for i in range(0, len(pais), 2):
            pai1 = pais[i]
            pai2 = pais[i + 1] if i + 1 < len(pais) else pais[i]

            filho = crossover(pai1, pai2)

            if random.random() < taxa_mutacao:
                filho = mutacao(filho, componentes, taxa_mutacao)

            proxima_geracao.append(filho)

            custo_filho = calcular_custo_total(filho, componentes)
            pontuacao_filho = calcular_pontuacao_total(filho, componentes, peso_pontuacoes)
            if custo_filho < limite_valor and pontuacao_filho > pontuacao_melhor_config:
                melhor_config = copy.deepcopy(filho)
                custo_melhor_config = custo_filho
                pontuacao_melhor_config = pontuacao_filho

        populacao = proxima_geracao

    return melhor_config, custo_melhor_config, pontuacao_melhor_config
