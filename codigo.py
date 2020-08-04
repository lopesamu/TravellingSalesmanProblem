#database used: burma14.tsp
#shortest route: 30.878500

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
        # select os individuos mais aptos (menor distancia percorrida)
        population = Select(population, f)
        
        # aplicar crossover e mutacao
        population = Reproduce(population, numInd, numCities, probCross, probMut)

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


# function that evaluates the population by means of euclidean distance - OK
def EvaluatePopulation(population, city, numInd, numCities):

    # f stores the total distance of each individual from population
    f = []

    # for each population[i], calculate the total distance
    for i in range(0, numInd):
        distance = RouteDistance(population[i], city, numCities)
        f.append(distance)

    return f


# function that selects the most suitable individuals - OK
def Select(population, f):
    
    indNewPopulation = []

    # select the shortest route through Elitism
    for i in range(len(f)):
        if f[i] == min(f):
            indNewPopulation.append(i)
            break

    # select routes through Tournament (n = 3)
    for i in range(1, len(f)):
        # draw n individuals from the current population
        n = 3
        draw = random.sample(range(len(f)),n)

        # between the selected individuals, choose the one with the shortest distance
        menor = f[draw[0]]
        indShortest = draw[0]
        for j in range(1, n):
            if menor > f[draw[j]]:
                menor = f[draw[j]]
                indShortest = draw[j]

        # indNewPopulation stores the indices of the new population
        indNewPopulation.append(indShortest)

    # create the new population
    newPopulation = []
    for i in range(0, len(indNewPopulation)):
        newPopulation.append(population[indNewPopulation[i]])
    newPopulation = np.array(newPopulation)

    return newPopulation


# aplica crossover na population
def Reproduce(population, numInd, numCities, probCross, probMut):

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
    numIter = 100

    # crossover and mutation rate
    probCross = 0.9
    probMut = 0.4
    
    # size of the population
    numInd = 30
    
    # read file with city coordinates which each line represents the coordinate x and y of a city
    city = np.loadtxt('cities.csv', delimiter=',')

    # measure the shortest route
    TravellingSalesman(city, numIter, probCross, probMut, numInd)

if __name__ == "__main__":
    main()
