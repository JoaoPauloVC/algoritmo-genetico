import random

## 1a - Cria população Inicial
def cria_populacao(tamanho_populacao, intervalo, dimensao):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = []
        for _ in range(dimensao):
            individuo.append(random.uniform(*intervalo))
        populacao.append(individuo)

    return populacao

## 1b - Avalia a população
def avalia_populacao(populacao):
    ## Lista de Valor da função objetivo de cada indivíduo
    aptidoes = [] 
    
    # Avalia a aptidão (valor da função a ser minimizada) de cada indivíduo na população
    for individuo in populacao:
        aptidao = funcao_objetivo(individuo)
        aptidoes.append(aptidao)
    return aptidoes

## 2a - Seleciona pais 
## OBS: Seleção de feitas feita por Torneio
def selecao_pais(populacao, aptidoes, qtd_pares, tamanho_torneio):
    pares_pais = []                 ## Lista com pares de pais
    
    for _ in range(qtd_pares):
        
        ## Númeor de participantes definido por tamanho_torneio e qualquer indivíduo da população pode ser escolhido.
        participantes_torneio = random.sample(range(len(populacao)), tamanho_torneio)
        
        ## Tupla com os 2 melhores indivíduos (menores valores de função objetivo) para serem pais.
        melhores_participantes = sorted(participantes_torneio, key=lambda i: aptidoes[i])[:2] 
        
        pares_pais.append(melhores_participantes)

    return pares_pais ## Retorna índice dos pais na população

## 2b - Realiza reprodução
def reproducao(populacao, indice_pais):
    
    ## Lista com par de filhos
    filhos = []                     
    
    
    ## Crossover.
        ## filho 1 (gene0, gene1) = (gene 0 pai 0, gene 1 pai 1 )
        ## filho 2 (gene0, gene1) = (gene 0 pai 1, gene 1 pai 0 )
    filho1 = [populacao[indice_pais[0]][0], populacao[indice_pais[1]][1]]
    filhos.append(filho1)
    
    filho2 = [populacao[indice_pais[0]][1], populacao[indice_pais[1]][0]]
    filhos.append(filho2)
    
    return filhos

## 2c - Avalia indivíduo
def avalia_individuo(descendente):
    aptidao_individuo = funcao_objetivo(descendente)
    return aptidao_individuo

## 3 - Seleciona indivíduos para realizar mutação e reavalia os mutados
def mutacao(descendentes, chance_mutacao, dominio):
    for i, (individuo, aptidao) in enumerate(descendentes):
        if chance_mutacao > random.random():
            for j in range(len(individuo)):
                individuo[j] += random.uniform(-0.1, 0.1)
                individuo[j] = max(dominio[0], min(dominio[1], individuo[j]))
            
            descendentes[i] = (individuo, avalia_individuo(individuo))  # Recalcula a aptidão após a mutação
            
    return descendentes
            
## 4 - Une todas as populações (população do início da iteração + descendentes ) e seleciona nova_população com melhores indivíduos e tamanho da população proposto
def substituicao(populacao, aptidoes, descendentes, aptidoes_descendentes, tamanho_populacao):
    # Combina a população atual com os descendentes
    nova_populacao = populacao + descendentes
    nova_aptidoes = aptidoes + aptidoes_descendentes

    # Ordene a nova população com base nas aptidões
    nova_populacao = [individuo for _, individuo in sorted(zip(nova_aptidoes, nova_populacao))]
    
    # Mantém apenas os melhores indivíduos para o 'tamanho_populacao'
    nova_populacao = nova_populacao[:tamanho_populacao]
    
    return nova_populacao

## 5 - Se a condição de parada não for Satisfeita, volte a etapa 2
def criterio_parada(geracao_atual, max_geracoes):
    return geracao_atual == max_geracoes

## Função objetivo a ser minimizada
def funcao_objetivo(individuo):
    return individuo[0]*individuo[0]*individuo[0] + 5*individuo[1]*individuo[1] + 2*individuo[0]*individuo[1]
  
        
## Algoritmo Genético         
def main():
    tamanho_populacao = 500                 ## Tamanho Total da População
    dominio = (-2, 2)                       ## Domínio das variáveis
    numero_variaveis = 2                    ## Quantidade de Variáveis
    quantidade_geracoes = 100               ## Quantidade de Gerações que o problema terá
    chance_mutacao = 0.06                    ## Chance de um indivíduo sofrer mutação (MUDAR PARA FATOR FIXO)
    pares_pais = 100                        ## Quantidade de pares de pais que irão gerar filhos
    tamanho_torneio = 8                     ## Quantidade de indivíduos da população que participam da selação
    geracao_atual = 0                       ## Geração Inicial

    
    populacao = cria_populacao(tamanho_populacao, dominio, numero_variaveis)   ## Lista de indivíduos
    
    while not criterio_parada(geracao_atual, quantidade_geracoes):
        aptidoes = avalia_populacao(populacao)                                 ## Lista de valores da função nos pontos (indivíduos) da população.
        
        pais = selecao_pais(populacao, aptidoes, pares_pais, tamanho_torneio)  ## Lista com índice dos pais selecionados para reprodução (cada elemento desta lista é uma dupla de índice de pais)
        descendentes = []
        
        for par in pais:
            descendente1, descendente2 = reproducao(populacao, par)
            aptidao_descendente1 = avalia_individuo(descendente1)
            aptidao_descendente2 = avalia_individuo(descendente2)
            descendentes.append((descendente1, aptidao_descendente1))
            descendentes.append((descendente2, aptidao_descendente2))
        
        ## Faz mutação nos descendentes (em alguns deles)
        descendentes_mutados = mutacao(descendentes, chance_mutacao, dominio)
        
        ## Refaz a lista de descendentes, agora com os mutantes.
        descendentes_mutantes = [desc[0] for desc in descendentes_mutados]              
        
        ## Refaz a lista de aptidoes dos descendentes, agora com os mutantes.
        aptidoes_descendentes_mutantes = [desc[1] for desc in descendentes]         
        
        ## Atualiza a população, com indivíduos da última população e os descendentes (incluindo os mutados)
        populacao = substituicao(populacao, aptidoes, descendentes_mutantes, aptidoes_descendentes_mutantes, tamanho_populacao)
        
        geracao_atual += 1
    
    melhor_individuo = populacao[aptidoes.index(min(aptidoes))]
    print("Melhor solução encontrada:", melhor_individuo)
    print("Valor da função a ser minimizada:", min(aptidoes))


if __name__ == "__main__":
    main()
