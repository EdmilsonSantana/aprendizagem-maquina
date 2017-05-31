from Cromossomo import Cromossomo
from util import aleatorioMinMax, aleatorio

class Populacao(object):
  
  probabilidade_mutacao = 0.2
  log = "Geracao %d: \n%s"
  #probabilidade_selecao = 0.9
  
  def __init__(self):
    self.cromossomos = []
    
  def adicionar(self, cromossomo):
    self.cromossomos.append(cromossomo)
    
  def evoluir(self,iteracoes):
    geracao = 1
    print(Populacao.log % (geracao, self.__str__()))
    if(len(self.cromossomos) % 2 == 0):
      while(geracao <= iteracoes and not self.achouObjetivo()):
        vencedores = self.torneio()
        self.cromossomos = self.selecao(vencedores)
        geracao += 1
        print(Populacao.log % (geracao, self.__str__()))
        
    return self.cromossomos
     
  def selecao(self, vencedores):
    selecao = []
    for i in range(0, len(vencedores), 2):
      filhoA, filhoB = Cromossomo.reproduzir(vencedores[i], vencedores[i+1])
      selecao.append(self.mutacao(filhoA))
      selecao.append(self.mutacao(filhoB))
      
    return selecao
    
  def mutacao(self, cromossomo):
    if(aleatorio() < Populacao.probabilidade_mutacao):
      cromossomo.mutacao()
    return cromossomo
    
  def torneio(self):
    pares = self.getParesTorneio()
    return [self.getMelhorPar(x, y) for x, y in pares]
    
  def getMelhorPar(self, x, y):
      aptidaoX = x.fitness()
      aptidaoY = y.fitness()
      par = {aptidaoY: y, aptidaoX: x}
      fitness = min(aptidaoX, aptidaoY)
      return par[fitness]
      
  def getParesTorneio(self):
    max = len(self.cromossomos)
    return [self.getParTorneio(max - 1) for i in range(0, max)]
  
  def getParTorneio(self, max):
    min = 0
    return (self.cromossomos[aleatorioMinMax(min, max)], 
            self.cromossomos[aleatorioMinMax(min, max)])
  
  def achouObjetivo(self):
    achou = False 
    for cromossomo in self.cromossomos:
      achou = cromossomo.objetivo()
      if(achou):
        break
    return achou
    
  def __str__(self):
    return '\n'.join([cromossomo.__str__() for cromossomo in self.cromossomos])
  
  def __repr__(self):
    return self.cromossomos
  
  
  
  