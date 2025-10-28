import random
import time

RANDOM_SEED = 42

class Node:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda: Node | None = None
        self.direita: Node | None = None
        self.altura: int = 1

class Arvore:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor):

        caminho: list[Node] = []
        # Se a raiz não existir, criamos uma
        if self.raiz is None:
            self.raiz = Node(valor)
            return

        # Se existir uma raiz, o nó atual recebe o valor da raiz
        no_atual = self.raiz

        while True:
            caminho.append(no_atual)
            # Se valor for menor que atual, olha para a esquerda do no_atual
            if valor < no_atual.valor:
                if no_atual.esquerda is None:
                    no_atual.esquerda = Node(valor)
                    break
                else:
                    no_atual = no_atual.esquerda

            # Se valor for maior que atual, olha para a direita do no_atual
            elif valor > no_atual.valor:
                if no_atual.direita is None:
                    no_atual.direita = Node(valor)
                    break
                else:
                    no_atual = no_atual.direita

            # Se o valor é igual ao atual ignora
            else:
                break

        caminho.reverse()
        for no_ancestral in caminho:
            self.atualizar_altura(no_ancestral)
            fator = self.obter_fator_balanceamento(no_ancestral)

            if fator > 1 or fator < -1:
                print("Desbalanceou meu brother")


    def rotacao_a_direta(self, z: Node):
        y = z.esquerda
        T3 = y.direita
        
        y.direita = z
        z.esquerda = T3

        self.atualizar_altura(z)
        self.atualizar_altura(y)

        return y
        
    def rotacao_a_esquerda(self, z: Node):
        y = z.direita
        T2 = y.esquerda
        
        y.esquerda = z
        z.direita = T2

        self.atualizar_altura(z)
        self.atualizar_altura(y)

        return y


    def buscar(self, valor):
        no_atual = self.raiz

        # Se não existe raiz não tem o que buscar
        if no_atual is None:
            return False

        while no_atual is not None:
            if valor == no_atual.valor:
                return True

            # Valor é menor
            elif valor < no_atual.valor:
                no_atual = no_atual.esquerda

            # Valor é maior
            else:
                no_atual = no_atual.direita

        # Valor não existe na árvore
        return False

    def obter_altura(self, no: Node | None):
        if no:
            return no.altura
        return 0

    def atualizar_altura(self, no: Node):

        altura_esquerda = self.obter_altura(no.esquerda)
        altura_direita  = self.obter_altura(no.direita)
        no.altura = 1 + max(altura_esquerda, altura_direita)

    def obter_fator_balanceamento(self, no: Node | None):
        if no is None:
            return 0

        return (self.obter_altura(no.esquerda) - self.obter_altura(no.direita))

# Função para testar a estrutura da árvore
def arvore_teste(valores):
    print("== TESTE DE ARVORE ==")
    arvore = Arvore()
    # Inserir valores na Árvore
    inicio_arvore = time.perf_counter()
    for valor in valores:
        arvore.inserir(valor)
    print(f"tempo construção {time.perf_counter() - inicio_arvore:.6f}\n")

    busca_todos_presentes(arvore, valores, "árvore")
    busca_todos_ausentes(arvore, valores, "árvore")

# Função para busca de valores presentes
def busca_todos_presentes(estrutura, valores, nome_estrutura):
    print(f"--- Busca Todos Presentes ({nome_estrutura}) ---")
    random.seed(RANDOM_SEED)
    busca = []
    for _ in range(10):
        indice = random.randint(0, len(valores) - 1)
        busca.append(valores[indice])
    inicio_busca = time.perf_counter()
    for n in busca:
        resposta = estrutura.buscar(n)
        print(f"O valor {n} está na {nome_estrutura}? {resposta}")
    print(f"tempo busca {time.perf_counter() - inicio_busca:.6f}\n")


# Função para busca de valores ausentes
def busca_todos_ausentes(estrutura, valores, nome_estrutura):
    print(f"--- Busca Todos Ausentes ({nome_estrutura}) ---")
    random.seed(RANDOM_SEED)
    busca = []
    for _ in range(10):
        busca.append(-random.randint(1, 1000))
    inicio_busca = time.perf_counter()
    for n in busca:
        resposta = estrutura.buscar(n)
        print(f"O valor {n} está na {nome_estrutura}? {resposta}")
    print(f"tempo busca {time.perf_counter() - inicio_busca:.6f}\n")


if __name__ == "__main__":

    arvore_teste([10, 5, 15, 3, 1, 20, 25, 18])

