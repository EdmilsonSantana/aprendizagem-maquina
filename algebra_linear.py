# -*- coding: utf-8 -*-
import csv, sys
  
def mutiplicacao_por_escalar(c, v):
    """c é um numero, v é um vetor"""
    return [c * v_i for v_i in v]
  
def somar_vetores(v, w):
    return [v_i + w_i for v_i, w_i in zip(v, w)]
  
def soma_dos_vetores(vetores):
  resultado = vetores[0]
  for vetor in vetores[1:]:
    resultado = somar_vetores(resultado, vetor)
  return resultado
  
def multiplicacao_vetores(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def soma_dos_quadrados(v):
    return multiplicar_vetores(v, v)
  
def subtrair_vetores(v, w):
  return [v_i - w_i for v_i, w_i in zip(v, w)]
          
def distancia_quadratica(v, w):
    return soma_dos_quadrados(subtrair_vetores(v, w))
          
def media_dos_vetores(vetores):
    escalar = 1.0/len(vetores)
    return mutiplicacao_por_escalar(escalar, soma_dos_vetores(vetores))