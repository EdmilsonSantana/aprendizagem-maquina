# -*- coding: utf-8 -*-

from Neuronio import Neuronio
from util import ler_csv
import numpy as np
import pandas as pd

class Rede(object):
  TAMANHO_MINIMO_CAMADAS = 2
  INDEX_CAMADA_ENTRADA = 0
  TAXA_APRENDIZADO = 0.6
  BIAS = [1]
  
  def __init__(self, entradas_treino, saidas_treino, neuronios_por_camada=[]):
    self.camadas = []
    self.entradas_treino = entradas_treino
    self.saidas_treino = saidas_treino
    self.inicializar_neuronios(neuronios_por_camada)
    
  def inicializar_neuronios(self,neuronios_por_camada):
    for quantidade_neuronios in neuronios_por_camada:
      camada = self.criar_camada(quantidade_neuronios)
      self.camadas.append(camada)

    self.ligar_camadas()

  def criar_camada(self, quantidade_neuronios):
    return [Neuronio(taxa_aprendizado=Rede.TAXA_APRENDIZADO) 
            for _ in range(quantidade_neuronios)]

  def adicionar_camada(self, quantidade_neuronios):
    camada = self.criar_camada(quantidade_neuronios)
    self.camadas.insert(0, camada)
   
  def ligar_camadas(self):
    for i, camada in enumerate(self.camadas):
      for neuronio in camada:
        quantidade_pesos = self.get_quantidade_pesos(i - 1)
        neuronio.inicializar_pesos(quantidade_pesos)
      
  def get_quantidade_pesos(self,posicao_camada):
    quantidade_pesos = None
    if posicao_camada < Rede.INDEX_CAMADA_ENTRADA:
      quantidade_pesos = self.get_tamanho_entrada()
    else:
      quantidade_pesos = len(self.camadas[posicao_camada])
    return quantidade_pesos
      
  def get_quantidade_camadas(self):
    return len(self.camadas)   
  
  def get_tamanho_entrada(self):
    return len(self.entradas_treino[0])
  
  def forward(self, entrada):
    saidas = []
    for camada in self.camadas:
      saida = [neuronio.ativacao(np.append(entrada, Rede.BIAS)) 
               for neuronio in camada]
      saidas.append(saida)
      entrada = saida
    return saidas
  
  def treinar(self, iteracoes):
    
    if self.get_quantidade_camadas() >= Rede.TAMANHO_MINIMO_CAMADAS:
      
      c = 0
      while c < iteracoes:
        for i, entradas in enumerate(self.entradas_treino):
          saidas_por_camada = self.forward(entradas)
          self.backpropagate(entradas, saidas_por_camada, 
                             self.saidas_treino[i])
        c += 1
        print(c)
    return self.camadas

  def backpropagate(self, entradas, saidas_por_camada, saidas_esperadas):
    
    gradiente = None
    posicao_camada = self.get_quantidade_camadas() - 1
    
    for _ in range(self.get_quantidade_camadas()):
      gradiente = self.get_gradiente(saidas_por_camada[posicao_camada],
                                     saidas_esperadas, 
                                     posicao_camada,
                                     gradiente)
            
      if posicao_camada == Rede.INDEX_CAMADA_ENTRADA:
          entrada_da_camada = entradas
      else:
          entrada_da_camada = saidas_por_camada[posicao_camada - 1]
        
      self.ajusta_pesos_camada(posicao_camada, entrada_da_camada, gradiente)
      posicao_camada -= 1
    
  
  def get_gradiente(self, saidas_da_camada, saidas_esperadas, 
                    posicao_camada, gradiente):
      derivada_sigmoid = self.derivada_sigmoid(saidas_da_camada)
      diferenca_saida = None
      if gradiente is None:
          diferenca_saida = np.subtract(saidas_da_camada, saidas_esperadas)
      else:
          pesos_camada_posterior = self.get_pesos_camada(posicao_camada + 1)
          diferenca_saida = np.dot(gradiente, pesos_camada_posterior)
        
      return np.multiply(derivada_sigmoid, diferenca_saida)
    
  def get_pesos_camada(self, posicao_camada):
      return np.array([neuronio.get_pesos() 
                       for neuronio in self.camadas[posicao_camada]])
                         
  def ajusta_pesos_camada(self, posicao_camada, entrada_da_camada, gradiente):
    camada = self.camadas[posicao_camada]
    for i, neuronio in enumerate(camada):
      for j, entrada in enumerate(entrada_da_camada + Rede.BIAS):
        neuronio.ajustar_peso(j, entrada, gradiente[i])
      
    
  def derivada_sigmoid(self, saidas_da_camada):
    return np.multiply(saidas_da_camada, np.subtract([1], saidas_da_camada)) 

  

if __name__ == "__main__":

   entradas_treino, saidas_treino = ler_csv("./datasets/ocupacao-treino.csv", ',', 6)
   entradas_teste, saidas_teste = ler_csv("./datasets/ocupacao-teste.csv", ',', 6)

   entradas_treino = entradas_treino.values
   saidas_treino = [[saida] for saida in saidas_treino.values]
   entradas_teste = entradas_teste.values
   saidas_teste = [[saida] for saida in saidas_teste.values]
   
   rede = Rede(entradas_treino, saidas_treino, [5, 5, 1])
    
   rede.treinar(10000)
   
   resultados = []
   
   for i, entrada in enumerate(entradas_teste):
       saidas = rede.forward(entrada)[-1]
       resultado = "%f, %d" % (round(saidas[0],2), saidas_teste[i][0])       
       resultados.append(resultado)   
   
   df = pd.DataFrame(resultados)     
   df.to_csv("./resultado.csv");    