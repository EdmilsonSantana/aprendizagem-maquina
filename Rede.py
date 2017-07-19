# -*- coding: utf-8 -*-
from sklearn.metrics import confusion_matrix
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from Neuronio import Neuronio
from util import ler_csv
import numpy as np
import pandas as pd

class Rede(object):
  TAMANHO_MINIMO_CAMADAS = 2
  INDEX_CAMADA_ENTRADA = 0
  TAXA_APRENDIZADO = 0.5
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
  
  def treinar(self, epocas, entradas_validacao, saidas_validacao):
    
    if self.get_quantidade_camadas() >= Rede.TAMANHO_MINIMO_CAMADAS:
        
      c = 0
      erros_treinamento = []
      erros_validacao = []
      while c < epocas:
        erro_treino = 0.0
        erro_validacao = 0.0
        # treino
        for i, entradas in enumerate(self.entradas_treino):
          saidas_por_camada = self.forward(entradas)
          erro_treino += self.backpropagation(entradas, saidas_por_camada, 
                                              self.saidas_treino[i])
        # validacao
        for i, entradas in enumerate(entradas_validacao):
          saidas_por_camada = self.forward(entradas)
          erro_validacao += self.get_erro_padrao(saidas_validacao[i], 
                                                 saidas_por_camada[-1])
        c += 1
        print(c)
        erros_validacao.append(erro_validacao / len(entradas_validacao))
        erros_treinamento.append(erro_treino / len(self.entradas_treino))
        
    return erros_treinamento, erros_validacao

  def backpropagation(self, entradas, saidas_por_camada, saidas_esperadas):
    
    gradiente = None
    posicao_camada = self.get_quantidade_camadas() - 1
    erros = []
    for _ in range(self.get_quantidade_camadas()):
      saidas_da_camada = saidas_por_camada[posicao_camada]
      
      gradiente = self.get_gradiente(saidas_da_camada,
                                     saidas_esperadas, 
                                     posicao_camada,
                                     gradiente)
                                     
      erros.append(self.get_erro_padrao(saidas_esperadas, saidas_da_camada))
  
      if posicao_camada == Rede.INDEX_CAMADA_ENTRADA:
          entrada_da_camada = entradas
      else:
          entrada_da_camada = saidas_por_camada[posicao_camada - 1]
        
      self.ajusta_pesos_camada(posicao_camada, entrada_da_camada, gradiente)
      posicao_camada -= 1
      
    return erros[0]
   
  
  def get_erro_padrao(self, saidas_esperadas, saidas_da_camada):
      diferenca_saida = np.subtract(saidas_esperadas, saidas_da_camada)
      return np.multiply(0.5, np.sum(np.power(diferenca_saida, 2.0)))
      
      
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

   entradas_treino, saidas_treino = ler_csv("./datasets/ocupacao-treino.csv", ',', 5)
   entradas_teste, saidas_teste = ler_csv("./datasets/ocupacao-teste.csv", ',', 5)
   entradas_validacao, saidas_validacao = ler_csv("./datasets/ocupacao-validacao.csv", ',', 5)

   entradas_treino = entradas_treino.values
   saidas_treino = [[saida] for saida in saidas_treino.values]

   entradas_teste = entradas_teste.values
   saidas_teste = saidas_teste.values
   
   entradas_validacao = entradas_validacao.values
   saidas_validacao = [[saida] for saida in saidas_validacao.values]

   rede = Rede(entradas_treino, saidas_treino, [6, 1])
    
   acerto_minimo = 0.9
   index_saida = 0
   epocas = 10000
   erros_treinamento, erros_validacao = rede.treinar(epocas, entradas_validacao, saidas_validacao)
   
   plt.xlabel("Épocas")
   plt.ylabel("Erro")
  
   plt.plot(np.arange(epocas) + 1, erros_treinamento, '-o')
   plt.plot(np.arange(epocas) + 1, erros_validacao, '-x')
   plt.legend(['Treinamento', 'Validação'], loc='upper right')
   plt.savefig('epocas-%d.png' % (epocas))
   
   saidas_obtidas = []
   for i, entrada in enumerate(entradas_teste):
       saidas = rede.forward(entrada)[-1]
       saida_obtida = saidas[index_saida]
       saidas_obtidas.append(1 if saida_obtida >= acerto_minimo else 0)
   
   matriz_confusao = confusion_matrix(saidas_teste, saidas_obtidas)
   df = pd.DataFrame(matriz_confusao)     
   df.to_csv("./matriz-confusao.csv"); 
   resultado_teste = {'Esperado':saidas_teste, 'Obtido':saidas_obtidas}
   df = pd.DataFrame(resultado_teste) 
   df.to_csv("./resultado_teste.csv");
   
   
   
   
   

def teste():
   raw_digits = [
          """11111
             1...1
             1...1
             1...1
             11111""",
             
          """..1..
             ..1..
             ..1..
             ..1..
             ..1..""",
             
          """11111
             ....1
             11111
             1....
             11111""",
             
          """11111
             ....1
             11111
             ....1
             11111""",     
             
          """1...1
             1...1
             11111
             ....1
             ....1""",             
             
          """11111
             1....
             11111
             ....1
             11111""",   
             
          """11111
             1....
             11111
             1...1
             11111""",             

          """11111
             ....1
             ....1
             ....1
             ....1""",
             
          """11111
             1...1
             11111
             1...1
             11111""",    
             
          """11111
             1...1
             11111
             ....1
             11111"""]     

   def make_digit(raw_digit):
       return [1 if c == '1' else 0
               for row in raw_digit.split("\n")
               for c in row.strip()]
                
   entradas_treino = list(map(make_digit, raw_digits))

   saidas_treino = [[1 if i == j else 0 for i in range(10)]
                   for j in range(10)]
               
   rede = Rede(entradas_treino, saidas_treino, [5, 10])
  
   epocas = 2000
   erros_treinamento = rede.treinar(epocas)
   
   plt.xlabel("Epocas")
   plt.ylabel("Erro Absoluto")
  
   plt.plot(np.arange(epocas) + 1, erros_treinamento, '-o')
   plt.savefig('epocas-%d.png' % (epocas))
   
   for i, entrada in enumerate(entradas_treino):
       saidas = rede.forward(entrada)[-1]
       print(i, [round(p,2) for p in saidas])
