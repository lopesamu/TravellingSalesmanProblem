# bibliotecas utilizadas
import numpy as np
import random
import math
import matplotlib.pyplot as plt

# ler arquivo com as coordenadas das cidades - cada linha representa a coordenada de uma cidade
cidade = np.loadtxt('cities.csv', delimiter=',')

#Classe que possui a solução do problema
class Solucao:
    def __init__(self, distancia, rota, eixoX, eixoY, resultados):
        self.distancia = distancia
        self.rota = rota
        self.eixoX = eixoX
        self.eixoY = eixoY
        self.resultados = resultados

class Filhos:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

# função principal
def caixeiro_viajante(qtde_individuos, prob_crossover, prob_mutacao, num_iter):

    # quantidade de cidades do problema
    num_cidades = len(cidade)

    # gera população inicial
    populacao = initializePopulation(qtde_individuos, num_cidades)

    # avalia a populacao inicial
    f = avaliar_populacao(populacao, cidade, qtde_individuos, num_cidades)

    resultado = []
    resultado.append(min(f))
    t = 1

    while t < num_iter:
        # selecionar os individuos mais aptos (menor distancia percorrida)
        populacao = selecionar(populacao, f)

        resultado.append(min(f))

        # aplicar crossover e mutacao
        populacao = reproduzir(populacao, qtde_individuos, num_cidades, prob_crossover, prob_mutacao)

        # avaliar a populacao gerada
        f = avaliar_populacao(populacao, cidade, qtde_individuos, num_cidades)

        # armazenar a menor rota encontrada
        if t == 1:
            menor_rota = np.array(populacao[0])
            distancia_menor_rota = f[0]
        elif distancia_menor_rota > min(f):
            menor_rota = np.array(populacao[0])
            distancia_menor_rota = f[0]

        # imprimir a iteração atual
        print("Iteração {}".format(t))

        t += 1

    # imprimir a rota encontrada
    eixo_x = []
    eixo_y = []

    for i in range(num_cidades):
        eixo_x.append(cidade[menor_rota[i]][0])
        eixo_y.append(cidade[menor_rota[i]][1])

    eixo_x.append(cidade[menor_rota[0]][0])
    eixo_y.append(cidade[menor_rota[0]][1])

    distancia_menor_rota = round(distancia_menor_rota,3)

    return Solucao(distancia_menor_rota, menor_rota, eixo_x, eixo_y, resultado)

# gera a populacao inicial aleatória - OK
def initializePopulation(qtde_individuos, num_cidades):
    populacao_inicial = []

    for i in range(qtde_individuos):
        populacao_inicial.append(random.sample(range(num_cidades), num_cidades))

    populacao_inicial = np.array(populacao_inicial)

    return populacao_inicial


# avalia a populacao por meio da distancia euclicidiana
def avaliar_populacao(populacao, cidade, qtde_individuos, num_cidades):

    # f armazena a distancia total de cada individuo da populacao
    f = []

    # para cada individuo da populacao, calcular distancia total
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

    ind_nova_populacao = []

    #Selecionar o individuo mais apto via elitismo
    primeiro_menor = min(f)
    indice_primeiro_menor = f.index(primeiro_menor)

    #Obtem o segundo menor
    fAux = np.delete(f, indice_primeiro_menor)
    segundo_menor = min(fAux)
    indice_segundo_menor = f.index(segundo_menor)

    #Adiciona ao array
    ind_nova_populacao.append(indice_primeiro_menor)
    ind_nova_populacao.append(indice_segundo_menor)

    # selecionar os individuos mais aptos via torneio
    for i in range(2, len(f)):
        # sortear n individuos da população atual
        n = 40
        sorteio = []
        for j in range(n):
            indice_sorteio = random.randint(0, len(f) - 1)
            sorteio.append(f[indice_sorteio])

        # dentre os individuos sorteados, escolher o que possui maior aptidão
        menor = min(sorteio)
        ind_menor = f.index(menor)


        # inserir o indice deste individuo em ind_nova_população
        ind_nova_populacao.append(ind_menor)

    # gerar a nova populacao
    nova_populacao = []
    for i in range(len(ind_nova_populacao)):
        nova_populacao.append(populacao[ind_nova_populacao[i]])
    
    return nova_populacao

# aplica crossover na populacao
def reproduzir(p, qtde_individuos, num_cidades, prob_crossover, prob_mutacao):

    # método de crossover - PMX do segundo artigo (aplicar nos individuos elitistas)
    elitista1 = np.array(p[0])
    elitista2 = np.array(p[1])

    i = 2
    while i < qtde_individuos:
        # gerar número aleatório r no intervalo [0, 1]
        r = random.random()

        # condição para haver crossover
        if r <= prob_crossover:
            f = crossover(p, num_cidades, i)
            p[i] = np.array(f.f1)
            p[i+1] = np.array(f.f2)

        i += 2


    # aplica mutacao
    for i in range(2, qtde_individuos):
        for j in range(0, num_cidades):
            r = random.random()

            # condicao para haver mutacao
            if r <= prob_mutacao:
                # seleciona duas cidades da populacao
                cidade1 = random.randint(0, num_cidades - 2)
                cidade2 = random.randint(cidade1, num_cidades - 1)

                #permuta os indices de cidade1 e cidade 2 no individuo
                aux = p[i][cidade1]
                p[i][cidade1] = p[i][cidade2]
                p[i][cidade2] = aux

        p[0] = np.array(elitista1)
        p[1] = np.array(elitista2)

    return p


def crossover(populacao, num_cidades, i):

    # determina os pontos de corte
    cp1 = random.randint(1, num_cidades - 2)
    cp2 = random.randint(cp1 + 1, num_cidades - 1)

    filho1 = populacao[i]
    filho2 = populacao[i + 1]

    # aplicar o crossover - permutar intervalo [cp1;cp2] entre filho1 e filho2
    aux = np.array(filho1)

    for j in range(cp1, cp2):
        filho1[j] = filho2[j]

    for j in range(cp1, cp2):
        filho2[j] = aux[j]

    # calcula elementos repetidos do filho1
    repetido_filho1=[]
    for j in range(0, cp1):
        for k in range(cp1, cp2):
            if filho1[j] == filho1[k]:
                repetido_filho1.append(j)
                break

    for j in range(cp2, num_cidades):
        for k in range(cp1, cp2):
            if filho1[j] == filho1[k]:
                repetido_filho1.append(j)
                break

    # calcula elementos repetidos do filho2
    repetido_filho2 = []
    for j in range(0, cp1):
        for k in range(cp1, cp2):
            if filho2[j] == filho2[k]:
                repetido_filho2.append(j)
                break

    for j in range(cp2, num_cidades):
        for k in range(cp1, cp2):
            if filho2[j] == filho2[k]:
                repetido_filho2.append(j,)
                break

    # inverte, par a par, os elementos repetidos nos filhos
    for j in range(len(repetido_filho1)):
        aux = filho1[repetido_filho1[j]]
        filho1[repetido_filho1[j]] = filho2[repetido_filho2[j]]
        filho2[repetido_filho2[j]] = aux

    return Filhos(filho1, filho2)


def main():
    # criterio de parada
    num_iter = 150
    # quantidade de individuos da população
    qtde_individuos = 800
    # taxas de crossover e de mutacao de mutação iniciais
    prob_crossover = 0.8
    prob_mutacao = 0.01

    melhor_resultado = caixeiro_viajante(qtde_individuos, prob_crossover, prob_mutacao, num_iter)

    plt.plot(melhor_resultado.eixoX, melhor_resultado.eixoY)
    plt.plot(melhor_resultado.eixoX, melhor_resultado.eixoY, "o")
    plt.title("Melhor resultado encontrado: {} - Rota: {}".format(melhor_resultado.distancia, melhor_resultado.rota))
    plt.show()

    xResultado = []
    for i in range(0, len(melhor_resultado.resultados)):
        xResultado.append(i)

    plt.plot(xResultado, melhor_resultado.resultados)
    plt.title("Resultados")
    plt.show()


if __name__ == "__main__":
    main()