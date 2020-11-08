# Versao 2, com kmeans++ implementado de forma adequada

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

# Preparaçao dos dados
localData = './observacoes.txt'
df = pd.read_csv(localData,sep = '  ',header=None) # Importando os dados
inData = df.values # Passando os dados do data frame para array
b = np.array([]) # Lista de grupos
cores = ['r','g','b','k','c','m','y','w']
qtdk = int(input('Digite a quantidade de centroides desejadas:')) # Quantidade de centroides
k = [] # Lista contendo os centroides
ciclos = []
mediaErro = []
x_Min = np.min(inData[:,0])
x_Max = np.max(inData[:,0])
y_Min = np.min(inData[:,1])
y_Max = np.max(inData[:,1])
print('Qual metodo deseja utilizar?\n[1] K_means tradicional\n[2] K_means ++')
metodo = int(input())


#Distancia euclidiana
def distanciaEuclid (sample, c):
    return sqrt(((inData[sample,0]-k[c][0])**2)+((inData[sample,1]-k[c][1])**2))

# Calculo da distancia minima euclidiana dentre os k's existentes
def minimoEuclid (sample):
    listadistancias = [] #lista auxiliar para comparar as distancias de cada centroide
    for c in range(qtdk): # Calculo da distancia para cada centroide
        listadistancias.append(distanciaEuclid(sample,c))
    return listadistancias.index(min(listadistancias)) # Retorna o indice da lista de distancias, que equivale ao respectivo k

# Atribui o index dos grupos em b
def ajustab ():
    b = np.array([]) # Lista de grupos
    for sample in range(len(inData)):
        b = np.append(b,minimoEuclid(sample))
    return b

# Atualizar os valores de cada centroide
def train(inData,qtdk,k):
    erroquadratico = []
    b = ajustab()
    for c in range(qtdk): # Roda por cada centroide (grupo)
        xlista = [] # Zera a lista utlizada pelo centroide anterior
        ylista = []
        for sample in range(len(inData)):
            if b[sample] == c:            
                xlista.append(inData[sample,0])   # Para determinado grupo, percorre por todas as entradas...
                ylista.append(inData[sample,1])   # ...agrupando em uma lista os valores de X e Y correspondentes
                erro = (sqrt(((inData[sample,0]-k[c][0])**2)+((inData[sample,1]-k[c][1])**2)))**2
                erroquadratico.append(erro)
        k[c][0] = sum(xlista)/len(xlista)
        k[c][1] = sum(ylista)/len(ylista)
        plt.plot(k[c][0],k[c][1],color = cores[c],marker = '|') # Somente para vizualisar o caminho percorrido pelo centroide
    media = sum(erroquadratico)/len(erroquadratico)
    mediaErro.append(media)
    ciclos.append(len(mediaErro))


#Plotagem dos pontos com relaçao aos grupos
def newplot (inData,k):
    cores = ['r','g','b','k','c','m','y','w']
    b = ajustab()
    listacores = []
    for l in range(len(b)):
        listacores.append(cores[int(b[l])]) # Indica qual a cor do grupo que b[l] está indicando
        plt.plot(inData[l,0],inData[l,1],color = listacores[l],marker = '.')
    listacores = np.array(listacores)
    for l in range(len(k)):
        plt.grid(b=1)
        plt.plot(k[l][0],k[l][1],color = cores[l],marker = 's')
    plt.show()

######################### Inicializaçao das centroides ##########################
# Utilizando K_means traidicional
if metodo == 1:
    for i in range(qtdk):
        kx = np.random.uniform(x_Min,x_Max)
        ky = np.random.uniform(y_Min,y_Max)
        kxy = np.array([kx,ky])
        k.append(kxy)
    for l in range(len(k)):
        plt.plot(k[l][0],k[l][1],color = cores[l],marker = 's')

# Utilizando o K_means ++
elif metodo == 2:
    prob = np.random.uniform(0,len(inData),qtdk) # Inicia uma lista de pontos aleatorios da quantidade de centroides desejadas
    for i in range(qtdk):
        k.append(inData[int(prob[i])]) # Atribui os centroides aos pontos declarados acima
        listadistancias = []
        listaprobabilidade = []
        for sample in range(len(inData)):
            distancia = distanciaEuclid(sample,i) # Calculo da distancia euclidiana
            listadistancias.append(distancia**2) # Coloca a distancia de cada ponto com relaçao a centroide em uma lista
        for c in listadistancias:
            for l in range(int(c)):
                listaprobabilidade.append(c) # Cria uma lista em que cada falor, se repete na quantidade de seu inteiro (os que possuem maior distancia aparecerão mais vezes na lista)
        distChosen = listaprobabilidade[int(np.random.uniform(0,len(listaprobabilidade)-1))] # Escolhe uma distancia aleatoria dentro da lista (a lista é ponderada pela frequencia de cada distancia)
        pointChosen = listadistancias.index(distChosen) # Escolhe o ponto referente a aquela distancia
        k[i] = inData[pointChosen] # Atribui o ponto escolhido a centroide


# Plotagem inicial
for l in range(len(k)):# Plotagem das centroides
    plt.plot(k[l][0],k[l][1],color = cores[l],marker = 's') 
plt.grid(b = 1)
plt.plot(inData[:,0],inData[:,1],'.k')# Plotagem dos pontos
plt.show()

# Fase de utilizaçao do k_means
def start(inData,k,qtdk):   
    teste = 0
    testelim = int(input('Digite aqui a quantidade maxima de ciclos'))
    newplot(inData,k)
    while teste < testelim:
        print(teste+1)
        train(inData,qtdk,k)
        teste += 1
    
    newplot(inData,k)
    plt.grid(b = 1)
    plt.plot(ciclos,mediaErro)
    plt.xlabel('QTD ciclos')
    plt.ylabel('Média erro')
    plt.show()
    print('Visto que existem 200 erros quadráticos em cada ciclo (qtd de pontos), \
realizei o calculo do erro com a média do erro quadratico de cada ciclo')

start(inData,k,qtdk)
