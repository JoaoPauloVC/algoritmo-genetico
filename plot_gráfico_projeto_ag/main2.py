import random
import matplotlib.pyplot as plt
import numpy as np

def calculate_clustering_metric(population):
    x_values = [indiv[0] for indiv in population]
    y_values = [indiv[1] for indiv in population]

    x_std = np.std(x_values)
    y_std = np.std(y_values)

    return x_std, y_std


def plot_population(population, fitness_scores, dominio):
    x_values = [indiv[0] for indiv in population]
    y_values = [indiv[1] for indiv in population]

    # Normalize fitness scores to [0, 1]
    normalized_fitness = [(score - min(fitness_scores)) / (max(fitness_scores) - min(fitness_scores)) for score in fitness_scores]

    # Create a colormap ranging from blue to red
    colormap = plt.cm.RdBu
    colors = [colormap(score) for score in normalized_fitness]

    plt.clf()  # Clear the previous plot
    plt.scatter(x_values, y_values, c=colors)
    plt.colorbar(label='Normalized Fitness')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Population Visualization')
    plt.xlim(*dominio)  # Set the x-axis limits
    plt.ylim(*dominio)  # Set the y-axis limits
    plt.pause(0.01)  # Pause to update the plot
    plt.draw()

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
    # Avalia a aptidão (valor da função a ser minimizada) de cada indivíduo na população
    aptidoes = [] ## Valor da função com os genes do indivíduo
    for individuo in populacao:
        aptidao = funcao_objetivo(individuo)
        aptidoes.append(aptidao)
    return aptidoes


## 2 - Seleciona pais e realiza reprodução e avalia
def selecao_pais(populacao, aptidoes, qtd_pares, tamanho_torneio):
    pares_pais = []
    
    for _ in range(qtd_pares):
        participantes_torneio = random.sample(range(len(populacao)), tamanho_torneio)
        melhores_participantes = sorted(participantes_torneio, key=lambda i: aptidoes[i])[:2] ##Returna tupla com os 2 melhores indivíduos (menores valores) para serem pais.
        pares_pais.append(melhores_participantes)

    return pares_pais ## Retorna índice dos pais na população

def reproducao(populacao, indice_pais):
    filhos = []
    
    filho1 = [populacao[indice_pais[0]][0], populacao[indice_pais[1]][1]]
    filhos.append(filho1)
    
    filho2 = [populacao[indice_pais[0]][1], populacao[indice_pais[1]][0]]
    filhos.append(filho2)
    
    return filhos

def avalia_individuo(descendente):
    aptidao_individuo = funcao_objetivo(descendente)
    return aptidao_individuo

## 3 - Seleciona indivíduos para realizar mutação
def mutacao(descendentes, chance_mutacao, dominio):
    for i, (individuo, aptidao) in enumerate(descendentes):
        if chance_mutacao > random.random():
            for j in range(len(individuo)):
                individuo[j] += random.uniform(-0.1, 0.1)
                individuo[j] = max(dominio[0], min(dominio[1], individuo[j]))
            
            descendentes[i] = (individuo, avalia_individuo(individuo))  # Recalcula a aptidão após a mutação
            
    return descendentes
            

## 4 - Une todas as populações e seleciona npop melhores indivíduos
def substituicao(populacao, aptidoes, descendentes, aptidoes_descendentes, tamanho_populacao):
    # Combine a população atual com os descendentes
    nova_populacao = populacao + descendentes
    nova_aptidoes = aptidoes + aptidoes_descendentes

    # Ordene a nova população com base nas aptidões
    nova_populacao = [individuo for _, individuo in sorted(zip(nova_aptidoes, nova_populacao))]
    
    # Mantenha apenas os npop melhores indivíduos
    nova_populacao = nova_populacao[:tamanho_populacao]
    
    return nova_populacao


## 5 - Se a condição de parada não for Satisfeita, volte a etapa 2
def criterio_parada(geracao_atual, max_geracoes, populacao, epsilon):
    (std_var_x, std_var_y) = calculate_clustering_metric(populacao)
    return (geracao_atual == max_geracoes) or (std_var_x <= epsilon and std_var_y <= epsilon)

def funcao_objetivo(individuo):
    return 3*individuo[0] + (-5*individuo[1])*(-5*individuo[1])
        


def main():
    tamanho_populacao = 100                 ## Tamanho Total da População
    dominio = (-10, 10)                     ## Domínio das variáveis
    numero_variaveis = 2                    ## Quantidade de Variáveis
    quantidade_geracoes = 100               ## Quantidade de Gerações que o problema terá
    chance_mutacao = 0.6                    ## Chance de um indivíduo sofrer mutação
    pares_pais = 20                         ## Quantidade de pares de pais que irão gerar filhos
    tamanho_torneio = 8                     ## Quantidade de indivíduos da população que participam da selação
    geracao_atual = 0                       ## Geração Inicial
    epsilon = 0.1

    # Activate interactive mode
    plt.ion()
    
    populacao = cria_populacao(tamanho_populacao, dominio, numero_variaveis)   ## Lista de indivíduos
    
    while not criterio_parada(geracao_atual, quantidade_geracoes, populacao, epsilon):
        aptidoes = avalia_populacao(populacao)                                 ## Lista de valores da função nos pontos (indivíduos) da população.
        
        pais = selecao_pais(populacao, aptidoes, pares_pais, tamanho_torneio)  ## Lista com índice dos pais selecionados para reprodução (cada elemento desta lista é uma dupla de índice de pais)
        descendentes = []
        
        for par in pais:
            descendente1, descendente2 = reproducao(populacao, par)
            aptidao_descendente1 = avalia_individuo(descendente1)
            aptidao_descendente2 = avalia_individuo(descendente2)
            descendentes.append((descendente1, aptidao_descendente1))
            descendentes.append((descendente2, aptidao_descendente2))
        
        descendentes_mutados = mutacao(descendentes, chance_mutacao, dominio)
        
        descendentes_mutantes = [desc[0] for desc in descendentes_mutados]              ## Refaz a lista de descendentes, agora com os mutantes.
        
        
        aptidoes_descendentes_mutantes = [desc[1] for desc in descendentes]         ## Refaz a lista de aptidoes, agora com os mutantes.
        
        
        populacao = substituicao(populacao, aptidoes, descendentes_mutantes, aptidoes_descendentes_mutantes, tamanho_populacao)
        
        plot_population(populacao, aptidoes, dominio)

        geracao_atual += 1
    
    melhor_individuo = populacao[aptidoes.index(min(aptidoes))]
    print("Melhor solução encontrada:", melhor_individuo)
    print("Valor da função a ser minimizada:", min(aptidoes))
    print(f"População convergiu em {geracao_atual} gerações")

    # Deactivate interactive mode at the end
    plt.ioff()
    plt.show()  # Keep the plot window open until manually closed


if __name__ == "__main__":
    main()