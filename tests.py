import numpy as np
import random

f = np.array([3,2,4])
population = np.array([[1,2,3,0],[0,1,2,3],[3,2,1,4],[1,3,2,0]])

# function that selects the most suitable individuals 
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


Select(population, f)