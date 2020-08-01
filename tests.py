import numpy as np
import random
populacao_inicial = []

# gerar um um caminho para cada individuo da população
indice_cidades = []
for i in range(0, 6):
    indice_cidades.append(i)

for i in range(0, 6):
    populacao_inicial.append(random.sample(indice_cidades, 6))

print(isinstance(populacao_inicial, list))

populacao_inicial = np.array(populacao_inicial, int)

print(populacao_inicial[0].dtype)