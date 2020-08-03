# libraries used
import numpy as np
import random
import math

def TravellingSalesman(city, numIter, probCross, probMut, numInd):
    # number of problem's cities
    numCities = len(city)

    # initialize the population
    populacao = InitializePopulation(numInd, numCities)

    # assess the initial population 
    f = avaliar_populacao(populacao, city, numInd, numCities)

    t = 0

    while t < numIter:
        # selecionar os individuos mais aptos (menor distancia percorrida)
        populacao = selecionar(populacao, f)

        # aplicar crossover e mutacao
        populacao = reproduzir(populacao, numInd, numCities, probCross, probMut)

        # avaliar a populacao gerada
        f = avaliar_populacao(populacao, city, numInd, numCities)

        if t == 0:
            menor_distancia = min(f)
        else:
            if min(f) < menor_distancia:
                menor_distancia = min(f)

        print("Iteração {} - Menor distancia encontrada: {}".format(t, menor_distancia))

        t += 1


# Function that returns the initial population - OK
def InitializePopulation(numInd, numCities):
    initialPopulation = []

    initialRoute = []
    for i in range(numCities):
        initialRoute.append(i)

    for i in range(numInd):
        initialPopulation.append(random.sample(initialRoute, numCities))

    initialPopulation = np.array(initialPopulation)

    return initialPopulation


# avalia a populacao por meio da distancia euclicidiana
def avaliar_populacao(populacao, city, qtde_individuos, numCities):

    # f armazena a distancia total de cada individuo da populacao
    f = []

    #para cada individuo da populacao, calcular distancia total
    for i in range(0, qtde_individuos):
        seq_citys = populacao[i]
        distancia = 0
        for j in range(1, numCities):
            aux = math.pow(city[seq_citys[j]][0] - city[seq_citys[j - 1]][0], 2) + \
                  math.pow(city[seq_citys[j]][1] - city[seq_citys[j - 1]][1], 2)
            distancia += math.sqrt(aux)

        # calcular a distância da última city visitada com a city de origem
        aux = math.pow(city[seq_citys[numCities - 1]][0] - city[seq_citys[0]][0], 2) + \
              math.pow(city[seq_citys[numCities - 1]][1] - city[seq_citys[0]][1], 2)
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
def reproduzir(populacao, qtde_individuos, numCities, probCross, probMut):

    # aplica crossover
    i = 0
    while i < qtde_individuos:
        # gerar número aleatório r no intervalo [0, 1]
        r = random.random()

        # condição para haver crossover
        if r <= probCross:
            populacao = crossover(populacao, numCities, i)

        i += 2

    # aplica mutacao
    for i in range(0, qtde_individuos):
        for j in range(0, 0, numCities):
            r = random.random()

            # condicao para haver mutacao
            if r <= probMut:
                # seleciona duas citys da populacao
                city1 = random.randint(0, numCities - 1)
                city2 = random.randint(0, numCities - 1)

                #permuta os indices de city1 e city 2 no individuo
                populacao[i][city1] = city2
                populacao[i][city2] = city1

    return populacao


def crossover(populacao, numCities, i):

    cp = random.randint(1, numCities - 2)

    pai1 = populacao[i]
    pai2 = populacao[i + 1]

    # gerar os novos filhos
    aux = pai1

    # gerar pai1
    for j in range(0, cp):
        pai1[j] = aux[j]
    for j in range(cp, numCities):
        pai1[j] = pai2[j]

    # gerar pai2
    for j in range(0, cp):
        pai2[j] = pai2[j]
    for j in range(cp, numCities):
        pai2[j]= aux[j]

    populacao[i] = pai1
    populacao[i + 1] = pai2

    return populacao


def main():
    # number of iterations
    numIter = 25

    # crossover and mutation rate
    probCross = 0.6
    probMut = 0.02
    
    # size of the population
    numInd = 30
    
    # read file with city coordinates which each line represents the coordinate x and y of a city
    city = np.loadtxt('cities.csv', delimiter=',')

    # measure the shortest route
    TravellingSalesman(city, numIter, probCross, probMut, numInd)

if __name__ == "__main__":
    main()
