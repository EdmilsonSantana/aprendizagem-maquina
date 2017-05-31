from Populacao import Populacao
from Rainhas import Rainhas

if __name__ == "__main__":
  populacao = Populacao()

  populacao.adicionar(Rainhas())
  populacao.adicionar(Rainhas())
  populacao.adicionar(Rainhas())
  populacao.adicionar(Rainhas())

  populacao.evoluir(1000)
  