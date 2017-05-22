from Populacao import Populacao
from Regioes import Regioes

if __name__ == "__main__":
  populacao = Populacao()

  populacao.adicionar(Regioes())
  populacao.adicionar(Regioes())
  populacao.adicionar(Regioes())
  populacao.adicionar(Regioes())

  populacao.evoluir(50)
  