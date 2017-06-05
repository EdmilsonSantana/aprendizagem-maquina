from Cromossomo import Cromossomo
from util import aleatorioMinMax, aleatorio

class Populacao(object):
  probabilidade_crossover = 0.9
  log = "Geracao %d: \n%s"
  
  def __init__(self, tipo, tamanho=0):
    self.cromossomos = [tipo() for _ in range(tamanho)]
    self.geracao = 1
    
  def adicionar(self, cromossomo):
    self.cromossomos.append(cromossomo)
    
  def evoluir(self,iteracoes):
    self.mensagem()
    if(len(self.cromossomos) % 2 == 0):
      while(self.geracao <= iteracoes and not self.achouObjetivo()):
        self.selecao()
        self.geracao += 1
        self.mensagem()
        
    return self.cromossomos
     
  def mensagem(self):
    print(Populacao.log % (self.geracao, self.__str__()))
    
  def selecao(self):
    vencedores = self.torneio()
    selecionados = []
    for i in range(0, len(vencedores), 2):
      filhoA, filhoB = self.crossover(vencedores[i], vencedores[i+1])
      filhoA, filhoB = self.mutacao(filhoA, filhoB)
      selecionados.append(filhoA)
      selecionados.append(filhoB)
    self.cromossomos = self.elitismo(self.cromossomos, selecionados)
      
  def crossover(self, paiA, paiB):
    filhoA = paiA
    filhoB = paiB
    if(aleatorio() <= Populacao.probabilidade_crossover):
      filhoA, filhoB = Cromossomo.reproduzir(paiA, paiB)
    return filhoA, filhoB
  
  def elitismo(self, pais, selecionados):
    pais = self.ordenarPorAptidao(pais)
    selecionados = self.ordenarPorAptidao(selecionados)
    selecionados[-1] = pais[0]
    return selecionados
   
  def ordenarPorAptidao(self, cromossomos):
    return sorted(cromossomos, key=lambda cromossomo: cromossomo.fitness())
    
  def mutacao(self, cromossomoA, cromossomoB):
    cromossomoA.mutacao()
    cromossomoB.mutacao()
    return cromossomoA, cromossomoB
    
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
        print("Em geracao %d: %s" % (self.geracao, cromossomo))
        break
    return achou
    
  def __str__(self):
    return '\n'.join([cromossomo.__str__() for cromossomo in self.cromossomos])
  
  def __repr__(self):
    return self.cromossomos
  
  
  
  