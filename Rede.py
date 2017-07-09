# -*- coding: utf-8 -*-

from Neuronio import Neuronio
from algebra_linear import multiplicacao_vetores
#from otimizacao.Cromossomo import Cromossomo

class Rede(object):
  TAMANHO_MINIMO_CAMADAS = 2
  INDEX_CAMADA_ENTRADA = 0
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
    return [Neuronio() for _ in range(quantidade_neuronios)]

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
      saida = [neuronio.ativacao(entrada + Rede.BIAS) for neuronio in camada]
      saidas.append(saida)
      entrada = saida
    return saidas
  
  def treinar(self, iteracoes):
    
    if self.get_quantidade_camadas() >= Rede.TAMANHO_MINIMO_CAMADAS:
      
      c = 0
      while c < iteracoes:
        
        for i, entrada in enumerate(self.entradas_treino):
          saidas_camadas = self.forward(entrada)
          self.backpropagate(entrada, saidas_camadas, self.saidas_treino[i])
   
        c += 1
    return self.camadas

  def backpropagate(self, entrada, saidas_por_camada, saida_esperada):
    
    gradiente_descendente = None
    posicao_camada = self.get_quantidade_camadas() - 1

    for _ in range(self.get_quantidade_camadas()):
      gradiente_descendente = self.get_gradiente_descendente(saidas_por_camada[posicao_camada],
                                                             posicao_camada, 
                                                             saida_esperada, 
                                                             gradiente_descendente)
      
     # print("Gradiente %s da Camada %d.\n" % (gradiente_descendente, posicao_camada + 1))
      
      entrada_da_camada = None
      if posicao_camada == Rede.INDEX_CAMADA_ENTRADA:
        entrada_da_camada = entrada
      else:
        entrada_da_camada = saidas_por_camada[posicao_camada - 1]
        
      self.ajusta_pesos_camada(self.camadas[posicao_camada], entrada_da_camada, gradiente_descendente)
      posicao_camada -= 1
      
      
  def get_gradiente_descendente(self, saidas_da_camada, posicao_camada, saida_esperada, gradiente_descendente=None):
    if posicao_camada == self.get_quantidade_camadas() - 1:
      diferenca_saida = lambda i:  saidas_da_camada[i] - saida_esperada[i]
    else:
      camada_posterior = self.camadas[posicao_camada + 1]
      diferenca_saida = lambda i: multiplicacao_vetores(gradiente_descendente, 
                                                        self.get_pesos_camada(camada_posterior, i))

    gradiente_descendente = [self.derivada_sigmoid(saida) * diferenca_saida(i)
                             for i, saida in enumerate(saidas_da_camada)]
    return gradiente_descendente
  
  def get_pesos_camada(self, camada, posicao_peso):
    return  [neuronio.get_peso(posicao_peso) for neuronio in camada]
  
  def ajusta_pesos_camada(self, camada, entrada_da_camada, gradiente_descendente):
    
    for i, neuronio in enumerate(camada):
      for j, entrada in enumerate(entrada_da_camada + Rede.BIAS):
        neuronio.ajustar_peso(j, entrada, gradiente_descendente[i])
      
    
  def derivada_sigmoid(self, x):
    return x * (1.0 - x) 
    
  def __repr__(self):
    return "%s\n" % ", ".join([neuronio for neuronio in camada
                              for camada in self.camadas])
    
if __name__ == "__main__":

  #entradas = [[1,0], [1,1], [0,1], [0,0]]
  #saidas = [[1], [0], [1], [0]]

  entradas = pd.read_csv('./datasets/ocupacao-treino.csv')
  print(entradas)
  #rede = Rede(entradas, saidas, [2, 2, 1])

  #print("Pesos %s" % (rede.treinar(10000)) )

  #for i, input in enumerate(entradas):
  #  outputs = rede.forward(input)[-1]
  #  print(i, [round(p,2) for p in outputs])
  


