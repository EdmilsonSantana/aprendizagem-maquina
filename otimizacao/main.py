from Populacao import Populacao
from Rainhas import Rainhas

if __name__ == "__main__":
  populacao = Populacao(Rainhas, 500)
  
  populacao.evoluir(20)
  