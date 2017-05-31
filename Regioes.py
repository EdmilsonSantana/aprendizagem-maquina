from Cromossomo import Cromossomo
from enum import Enum
from util import binToDec

class Regioes(Cromossomo):
  
  regioes = 5
  bits = 2
  
  def __init__(self):
    super(Regioes, self).__init__(Regioes.regioes, Regioes.bits)

  def fitness(self):
    return self.regioesEmConflito()
      
  def objetivo(self):
    return self.regioesEmConflito() == 0
  
  def regioesEmConflito(self):
    conflitos = 0
    for regiao in range(1, Regioes.regioes + 1):
      cor = self.getCorRegiao(regiao)
      conflitos += int(self.regiaoNaoPintada(cor))
      conflitos += int(cor == self.getCorRegiao(regiao - 1))
      conflitos += int(cor == self.getCorRegiao(regiao - 2))
      conflitos += int(cor == self.getCorRegiao(regiao + 1))
      conflitos += int(cor == self.getCorRegiao(regiao + 2))
    return conflitos
  
  def regiaoNaoPintada(self,cor):
    return cor == Cores.WHITE
  
  def getCorRegiao(self, regiao):
    cor = None
    if(regiao >= 1 and regiao <= Regioes.regioes):
      cor = self.getCor(self.getGene(regiao))
    return cor
  
  def getCor(self, regiao):
    return Cores(binToDec(regiao))

  def converterGene(self, posicao, regiao):
    return self.getCor(regiao).name
  
class Cores(Enum):
  WHITE = 0
  RED = 1
  GREEN = 2
  BLUE = 3
  
  

  
 