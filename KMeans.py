from algebra_linear import distancia_quadratica, media_dos_vetores
import random
from util import gerar_grafico, ler_csv, mostrar_grafico
from collections import Counter, defaultdict

class KMeans(object):
  def __init__(self, k):
    self.k = k
    self.agrupamentos = None
    
  def classificar(self, entrada):
    distancia = lambda i: distancia_quadratica(entrada, self.agrupamentos[i])
    return min(range(self.k), key=distancia)
  
  def treinar(self, entradas):
    self.agrupamentos = random.sample(entradas, self.k)
    atribuicoes = None
    while True:
      novas_atribuicoes = list(map(self.classificar, entradas))

      if novas_atribuicoes == atribuicoes:
        return
      
      atribuicoes = novas_atribuicoes
      
      for i in range(self.k):
        pontos = [p for p,a in zip(entradas, atribuicoes) if a == i] 
        if pontos:
          self.agrupamentos[i] = media_dos_vetores(pontos)

  def agrupar(self, entradas):
    classificacoes = [self.classificar(entrada) for entrada in entradas]
    grupos = defaultdict(list)
    for classificacao, entrada in zip(classificacoes, entradas):
      grupos[classificacao].append(entrada)
    return grupos



if __name__ == "__main__":           
  
  entradas, classificacoes = ler_csv("datasets/clusterizacao.csv", ';', 2)
  x = entradas.iloc[:, 0]
  y = entradas.iloc[:, 1]
  lista_entradas = entradas.values.tolist()

  def clusterizacao(k, entradas):
    kMeans = KMeans(k)
    cores = [i * 20 for i in range(1, k + 1)]
    kMeans.treinar(entradas)
    gerar_grafico("Cluster %d" % (k), x, y, [cores[kMeans.classificar(entrada)] 
                                             for entrada in entradas])
    grupos = kMeans.agrupar(entradas)
    i = 0
    while i < k:
      print(kMeans.agrupamentos[i])
      print(len(grupos[i]))
      i += 1

  clusterizacao(2, lista_entradas)


  

  

 
  
  



    
        
      