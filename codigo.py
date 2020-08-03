# libraries used
import numpy as np
import random
import math

def TravellingSalesman(city, numIter, probCross, probMut, numInd):
    # number of problem's cities
    numCities = len(city)

    # initialize the population
    population = InitializePopulation(numInd, numCities)

    # evaluate the initial population 
    f = EvaluatePopulation(population, city, numInd, numCities)

    t = 0

    while t < numIter:
        # selecionar os individuos mais aptos (menor distancia percorrida)
        population = selecionar(population, f)

        # aplicar crossover e mutacao
        population = reproduzir(population, numInd, numCities, probCross, probMut)

        # avaliar a population gerada
        f = EvaluatePopulation(population, city, numInd, numCities)

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


# function that calculates the route's distance - OK
def RouteDistance(route, city, numCities):
    distance = 0
    for i in range(1, numCities):
        aux = math.pow(city[route[i]][0] - city[route[i - 1]][0], 2) + math.pow(city[route[i]][1] - city[route[i - 1]][1], 2)
        distance += math.sqrt(aux)

    # calculate the distance from the last city visited to the city of origin
    aux = math.pow(city[route[numCities - 1]][0] - city[route[0]][0], 2) + math.pow(city[route[numCities - 1]][1] - city[route[0]][1], 2)
    distance += math.sqrt(aux)

    return distance


# function that evaluates the population by means of euclidean distance
def EvaluatePopulation(population, city, numInd, numCities):

    # f stores the total distance of each individual from population
    f = []

    # for each population[i], calculate the total distance
    for i in range(0, numInd):
        distance = RouteDistance(population[i], city, numCities)
        f.append(distance)

    return f


# seleciona os individuos mais aptos via torneio e elitismo
def selecionar(population, f):

    # selecionar o individuo mais apto via elitismo
    ind_nova_population = []

    for i in range(0, len(f)):
        if f[i] == min(f):
            ind_nova_population.append(i)
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
        ind_nova_population.append(ind_menor)

    # gerar a nova population
    nova_population = []
    for i in range(0, len(ind_nova_population)):
        nova_population.append(population[ind_nova_population[i]])

    return nova_population

# aplica crossover na population
def reproduzir(population, numInd, numCities, probCross, probMut):

    # aplica crossover
    i = 0
    while i < numInd:
        # gerar número aleatório r no intervalo [0, 1]
        r = random.random()

        # condição para haver crossover
        if r <= probCross:
            population = crossover(population, numCities, i)

        i += 2

    # aplica mutacao
    for i in range(0, numInd):
        for j in range(0, 0, numCities):
            r = random.random()

            # condicao para haver mutacao
            if r <= probMut:
                # seleciona duas citys da population
                city1 = random.randint(0, numCities - 1)
                city2 = random.randint(0, numCities - 1)

                #permuta os indices de city1 e city 2 no individuo
                population[i][city1] = city2
                population[i][city2] = city1

    return population


def crossover(population, numCities, i):

    cp = random.randint(1, numCities - 2)

    pai1 = population[i]
    pai2 = population[i + 1]

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

    population[i] = pai1
    population[i + 1] = pai2

    return population


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
