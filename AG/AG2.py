import random
import copy

def selecionar_pais(populacao, componentes, peso_pontuacoes):
    pontuacoes = [calcular_pontuacao_total(individuo, componentes, peso_pontuacoes) for individuo in populacao]
    total_pontuacao = sum(pontuacoes)
    probabilidades = [p / total_pontuacao for p in pontuacoes]
    pais = random.choices(populacao, weights=probabilidades, k=len(populacao))
    return pais

def criar_configuracao_aleatoria(componentes, limite_valor):
    configuracao = {}
    for tipo, opcoes in componentes.items():
        opcoes_abaixo_do_limite = [comp for comp in opcoes if opcoes[comp]["price"] <= limite_valor]
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
        scores = [comp["score"] for comp in componentes[tipo].values()]
        min_score, max_score = min(scores), max(scores)
        score = componentes[tipo][escolha]["score"]
        score_normalizado = (score - min_score) / (max_score - min_score) if max_score > min_score else 0
        peso = peso_pontuacoes.get(tipo, 1)
        pontuacao_total += score_normalizado * peso
    return pontuacao_total

def crossover(configuracao1, configuracao2):
    nova_configuracao = copy.deepcopy(configuracao1)
    ponto_crossover = random.choice(list(configuracao1.keys()))
    for tipo in configuracao1:
        if tipo == ponto_crossover:
            nova_configuracao[tipo] = configuracao2[tipo]
    return nova_configuracao

def mutacao(configuracao, componentes, taxa_mutacao):
    if random.random() < taxa_mutacao:
        tipo_mutacao = random.choice(list(configuracao.keys()))
        opcoes_abaixo_do_limite = [comp for comp in componentes[tipo_mutacao] if componentes[tipo_mutacao][comp]["price"] <= calcular_custo_total(configuracao, componentes)]
        if opcoes_abaixo_do_limite:
            escolha_mutacao = random.choice(opcoes_abaixo_do_limite)
            configuracao[tipo_mutacao] = escolha_mutacao
    return configuracao

def algoritmo_genetico(componentes, limite_valor, peso_pontuacoes, geracoes=100000, tamanho_populacao=100000, taxa_mutacao=0.9):
    populacao = [criar_configuracao_aleatoria(componentes, limite_valor) for _ in range(tamanho_populacao)]

    melhor_config = None
    custo_melhor_config = float('inf')
    pontuacao_melhor_config = float('-inf')

    for geracao in range(geracoes):
        populacao = sorted(populacao, key=lambda x: calcular_custo_total(x, componentes))

        pais = selecionar_pais(populacao, componentes, peso_pontuacoes)
        proxima_geracao = []

        for i in range(0, len(pais) - 1, 2):
            pai1 = pais[i]
            pai2 = pais[i + 1]

            filho = crossover(pai1, pai2)

            filho = mutacao(filho, componentes, taxa_mutacao)

            proxima_geracao.append(filho)

            custo_filho = calcular_custo_total(filho, componentes)
            pontuacao_filho = calcular_pontuacao_total(filho, componentes, peso_pontuacoes)
            if custo_filho < limite_valor and pontuacao_filho > pontuacao_melhor_config:
                melhor_config = copy.deepcopy(filho)
                custo_melhor_config = custo_filho
                pontuacao_melhor_config = pontuacao_filho

        populacao = proxima_geracao

        # Adicione uma condição de parada antecipada, se necessário
        if pontuacao_melhor_config >= 1.0:  # Exemplo: condição para parar se a pontuação for ótima
            break

    return melhor_config, custo_melhor_config, pontuacao_melhor_config
