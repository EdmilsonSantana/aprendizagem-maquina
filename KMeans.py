from algebra_linear import distancia_quadratica, media_dos_vetores
import random

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
      novas_atribuicoes = map(self.classificar, entradas)
      
      if novas_atribuicoes == atribuicoes:
        return
      
      atribuicoes = novas_atribuicoes
      
      for i in range(self.k):
        pontos = [p for p,a in zip(entradas, atribuicoes) if a == i] 
        if pontos:
          self.agrupamentos[i] = media_dos_vetores(pontos)

if __name__ == "__main__":           
  inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],
            [26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],
            [-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]
  random.seed(0) 
  kMeans = KMeans(2)
  kMeans.treinar(inputs)
  print kMeans.agrupamentos
    
        
      