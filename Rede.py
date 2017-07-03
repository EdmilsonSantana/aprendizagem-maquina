# -*- coding: utf-8 -*-

from Neuronio import Neuronio
from algebra_linear import multiplicacao_vetores

class Rede(object):
  TAMANHO_MINIMO_CAMADAS = 2
  INDEX_CAMADA_ENTRADA = 0
  BIAS = [1]
  
  def __init__(self, tamanho_saida, tamanho_entrada):
    self.camadas = []
    self.tamanho_entrada = tamanho_entrada
    self.tamanho_saida = tamanho_saida
    self.adicionar_camada(tamanho_saida)
    
  def criar_camada(self, tamanho):
    return [Neuronio() for _ in range(tamanho)]

  def adicionar_camada(self, tamanho):
    camada = self.criar_camada(tamanho)
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
    return self.tamanho_entrada
  
  def forward(self, entrada):
    saidas = []
    for camada in self.camadas:
      saida = [neuronio.ativacao(entrada + Rede.BIAS) for neuronio in camada]
      saidas.append(saida)
      entrada = saida
    return saidas
  
  def treinar(self,entradas, saidas, iteracoes):
    
    if self.get_quantidade_camadas() >= Rede.TAMANHO_MINIMO_CAMADAS:
      
      self.ligar_camadas()
      c = 0
      while c < iteracoes:
        print("Iteração %d\n" % (c + 1))
        for i, entrada in enumerate(entradas):
          print("Entrada: %s\n" % (entrada))
          saidas_camadas = self.forward(entrada)
          print("Saída: %s\n" % (saidas_camadas[-1]))
          self.backpropagate(entrada, saidas_camadas, saidas[i])
          
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
      
      print("Gradiente %s da Camada %d.\n" % (gradiente_descendente, posicao_camada + 1))
      
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
    
    
rede = Rede(10, 25)
rede.adicionar_camada(5)

entradas = [[1,0], [1,1], [0,1], [0,0]]
saidas_esperadas = [[1], [0], [1], [0]]

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
                
inputs = map(make_digit, raw_digits)

targets = [[1 if i == j else 0 for i in range(10)]
            for j in range(10)]

rede.treinar(inputs, targets, 10000)

for i, input in enumerate(inputs):
  outputs = rede.forward(input)[-1]
  print i, [round(p,2) for p in outputs]
  

