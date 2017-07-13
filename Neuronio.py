# -*- coding: utf-8 -*-

import math
import numpy as np

class Neuronio(object):
  def __init__(self, sinapses=0, taxa_aprendizado=1):
    self.taxa_aprendizado = taxa_aprendizado
    if sinapses > 0:
      self.inicializar_pesos(sinapses)
    
  def inicializar_pesos(self, sinapses):
    self.pesos = np.random.rand(sinapses + 1)
  
  def ativacao(self, entradas):
    return self.sigmoid(np.dot(entradas, self.pesos))
  
  def get_peso(self,index):
    return self.pesos[index]
    
  def get_pesos(self):
      return self.pesos[:-1]
  
  def ajustar_peso(self, index, entrada, gradiente):
    self.pesos[index] -= entrada * gradiente * self.taxa_aprendizado
    
  def sigmoid(self, x):
    return 1.0 / (1.0 + math.exp(-x))
    