# -*- coding: utf-8 -*-

import math
from algebra_linear import multiplicacao_vetores
from random import random

class Neuronio(object):
  TAXA_APRENDIZADO = 0.6
  def __init__(self, sinapses=0):
    if sinapses > 0:
      self.inicializar_pesos(sinapses)
    
  def inicializar_pesos(self, sinapses):
    self.pesos = [random() for _ in range(sinapses + 1)]
  
  def ativacao(self, entradas):
    return self.sigmoid(multiplicacao_vetores(entradas, self.pesos))
  
  def get_peso(self,index):
    return self.pesos[index]
  
  def ajustar_peso(self, index, entrada, gradiente_descendente):
    self.pesos[index] -= entrada * gradiente_descendente * Neuronio.TAXA_APRENDIZADO
    
  def sigmoid(self, x):
    return 1.0 / (1.0 + math.exp(-x))
  
  def __repr__(self):
    return ", ".join([str(peso) for peso in self.pesos])