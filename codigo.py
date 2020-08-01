# bibliotecas utilizadas
import numpy as np
import random
import math

# ler arquivo com as coordenadas das cidades - cada linha representa a coordenada de uma cidade
cidade = np.loadtxt('cidades.csv', delimiter=',')

# função principal
def caixeiro_viajante():

    # criterio de parada
    num_iter = 5

    # taxa de crossover e de mutacao
    prob_crossover = 0.6
    prob_mutacao = 0.02

    # quantidade de cidades do problema
    num_cidades = len(cidade)

    # quantidade de individuos da população
    qtde_individuos = 6

    # gera população inicial
    populacao = InitializePopulation(qtde_individuos, num_cidades)

    # avalia a populacao inicial
    f = avaliar_populacao(populacao, cidade, qtde_individuos, num_cidades)

    t = 1

    while t < num_iter:
        # selecionar os individuos mais aptos (menor distancia percorrida)
        populacao = selecionar(populacao, f)

        # aplicar crossover e mutacao
        populacao = reproduzir(populacao, qtde_individuos, num_cidades, prob_crossover, prob_mutacao)

        # avaliar a populacao gerada
        f = avaliar_populacao(populacao, cidade, qtde_individuos, num_cidades)

        if t == 1:
            menor_distancia = min(f)
        else:
            if min(f) < menor_distancia:
                menor_distancia = min(f)

        print("Iteração {} - Menor distancia encontrada: {}".format(t, menor_distancia))

        t += 1


# gera a populacao inicial - TUDO CERTO
def InitializePopulation(qtde_individuos, num_cidades):
    populacao_inicial = []

    # gerar um um caminho para cada individuo da população
    indice_cidades = []
    for i in range(0, num_cidades):
        indice_cidades.append(i)

    for i in range(0, qtde_individuos):
        populacao_inicial.append(random.sample(indice_cidades, num_cidades))

    populacao_inicial = np.array(populacao_inicial)

    return populacao_inicial


# avalia a populacao por meio da distancia euclicidiana
def avaliar_populacao(populacao, cidade, qtde_individuos, num_cidades):

    # f armazena a distancia total de cada individuo da populacao
    f = []

    #para cada individuo da populacao, calcular distancia total
    for i in range(0, qtde_individuos):
        seq_cidades = populacao[i]
        distancia = 0
        for j in range(1, num_cidades):
            aux = math.pow(cidade[seq_cidades[j]][0] - cidade[seq_cidades[j - 1]][0], 2) + \
                  math.pow(cidade[seq_cidades[j]][1] - cidade[seq_cidades[j - 1]][1], 2)
            distancia += math.sqrt(aux)

        # calcular a distância da última cidade visitada com a cidade de origem
        aux = math.pow(cidade[seq_cidades[num_cidades - 1]][0] - cidade[seq_cidades[0]][0], 2) + \
              math.pow(cidade[seq_cidades[num_cidades - 1]][1] - cidade[seq_cidades[0]][1], 2)
        distancia += math.sqrt(aux)

        f.append(distancia)

    return f


# seleciona os individuos mais aptos via torneio e elitismo
def selecionar(populacao, f):

    # selecionar o individuo mais apto via elitismo
    ind_nova_populacao = []

    for i in range(0, len(f)):
        if f[i] == min(f):
            ind_nova_populacao.append(i)
            break

    # selecionar os individuos mais aptos via torneio
    for i in range(1, len(f)):
        # sortear três individuos da população atual
        n = 3
        sorteio = []
        for j in range(0, n):
            sorteio.append(random.randint(0, len(f) - 1))

        # dentre os individuos sorteados, escolher o que possui maior aptidão
        menor = f[sorteio[0]]
        ind_menor = sorteio[0]
        for j in range(0, n):
            if menor < f[sorteio[j]]:
                menor = f[sorteio[j]]
                ind_menor = sorteio[j]

        # inserir o indice deste individuo em ind_nova_população
        ind_nova_populacao.append(ind_menor)

    # gerar a nova populacao
    nova_populacao = []
    for i in range(0, len(ind_nova_populacao)):
        nova_populacao.append(populacao[ind_nova_populacao[i]])

    return nova_populacao

# aplica crossover na populacao
def reproduzir(populacao, qtde_individuos, num_cidades, prob_crossover, prob_mutacao):

    # aplica crossover
    i = 0
    while i < qtde_individuos:
        # gerar número aleatório r no intervalo [0, 1]
        r = random.random()

        # condição para haver crossover
        if r <= prob_crossover:
            populacao = crossover(populacao, num_cidades, i)

        i += 2

    # aplica mutacao
    for i in range(0, qtde_individuos):
        for j in range(0, 0, num_cidades):
            r = random.random()

            # condicao para haver mutacao
            if r <= prob_mutacao:
                # seleciona duas cidades da populacao
                cidade1 = random.randint(0, num_cidades - 1)
                cidade2 = random.randint(0, num_cidades - 1)

                #permuta os indices de cidade1 e cidade 2 no individuo
                populacao[i][cidade1] = cidade2
                populacao[i][cidade2] = cidade1

    return populacao


def crossover(populacao, num_cidades, i):

    cp = random.randint(1, num_cidades - 2)

    pai1 = populacao[i]
    pai2 = populacao[i + 1]

    # gerar os novos filhos
    aux = pai1

    # gerar pai1
    for j in range(0, cp):
        pai1[j] = aux[j]
    for j in range(cp, num_cidades):
        pai1[j] = pai2[j]

    # gerar pai2
    for j in range(0, cp):
        pai2[j] = pai2[j]
    for j in range(cp, num_cidades):
        pai2[j]= aux[j]

    populacao[i] = pai1
    populacao[i + 1] = pai2

    return populacao


def main():
    caixeiro_viajante()

if __name__ == "__main__":
    main()
