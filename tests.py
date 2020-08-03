import math 
import numpy as np

city = np.array([[1,1],[2,2],[3,3]])
numCities = len(city)
route = np.array([2,0,1])

# function that calculates the route's distance
def RouteDistance(route, city, numCities):
    distance = 0
    for i in range(1, numCities):
        aux = math.pow(city[route[i]][0] - city[route[i - 1]][0], 2) + math.pow(city[route[i]][1] - city[route[i - 1]][1], 2)
        distance += math.sqrt(aux)

    # calculate the distance from the last city visited to the city of origin
    aux = math.pow(city[route[numCities - 1]][0] - city[route[0]][0], 2) + math.pow(city[route[numCities - 1]][1] - city[route[0]][1], 2)
    distance += math.sqrt(aux)

    return distance

RouteDistance(route, city, numCities)
