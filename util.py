# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

def mostrar_grafico(x, y, cores):
	plt.scatter(x, y, c=cores)
	plt.show()

def gerar_grafico(arquivo, x, y, cores):
	plt.scatter(x, y, c=cores)
	plt.savefig('%s.png' % (arquivo))

def ler_csv(arquivo, separator, colunaClassificacao):
	"""retorna um data frame para as entradas e outro para as classficações"""
	data_frame = pd.read_csv(arquivo, header=None, sep=separator)
	entradas = data_frame.iloc[:,0:colunaClassificacao]
	classificacoes = data_frame.iloc[:,colunaClassificacao]
	return entradas, classificacoes

def to_list(data_frame):
	return data_frame.values.tolist()
