from Cromossomo import Cromossomo
from util import binToDec

class Rainhas(Cromossomo):
  quantidade = 8
  bits = 3
  
  def __init__(self):
    super(Rainhas, self).__init__(Rainhas.quantidade, Rainhas.bits) 
  
  def fitness(self):
    return self.rainhasEmAtaque()
  
  def objetivo(self):
    return self.rainhasEmAtaque() == 0
  
  def rainhasEmAtaque(self):
    ataques = 0
    rainha = 1
    while(rainha <= Rainhas.quantidade):
      ataques += self.contarAtaques(rainha)
      rainha += 1
    return ataques
    
  def contarAtaques(self, rainha):
    vizinha = rainha + 1
    ataques = 0
    
    while(vizinha <= Rainhas.quantidade):
      emDiagonal = self.ataqueEmDiagonal(rainha, vizinha)
      emLinha = self.ataqueEmLinha(rainha, vizinha)
      if (emDiagonal or emLinha):
        ataques += 1
      vizinha += 1
      
    return ataques
      
    
  def ataqueEmDiagonal(self, rainha, vizinha):
    linha = binToDec(self.getGene(rainha)) + 1
    linhaVizinha = binToDec(self.getGene(vizinha)) + 1
    
    distanciaLinha = abs(linha - linhaVizinha)
    distanciaColuna = abs(rainha - vizinha)
    
    return distanciaLinha == distanciaColuna
    
    
  def ataqueEmLinha(self, rainha, vizinha):
    linha = self.getGene(rainha)
    linhaVizinha = self.getGene(vizinha)
    return linha == linhaVizinha
  
  def converterGene(self, posicao, gene):
    return "(%s, %s)" % (binToDec(gene) + 1, posicao)
    
    
    
    


    
  
