import random
import time

RANDOM_SEED = 42

class Node:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda: Node | None = None
        self.direita: Node | None = None
        self.altura: int = 1

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
        # Se a raiz não existir, criamos uma
        if self.raiz is None:
            self.raiz = Node(valor)
            return

        # Se existir uma raiz, o nó atual recebe o valor da raiz
        no_atual = self.raiz
        no_novo = Node(valor)
        caminho: list[Node] = []

        # Inserção normal
        while True:
            caminho.append(no_atual)

            if valor < no_atual.valor:
                if no_atual.esquerda is None:
                    no_atual.esquerda = no_novo
                    break
                else:
                    no_atual = no_atual.esquerda

            elif valor > no_atual.valor:
                if no_atual.direita is None:
                    no_atual.direita = no_novo
                    break
                else:
                    no_atual = no_atual.direita

            else:
                # Valor já existe, ignora
                return

        # Balanceamento: percorre do nó inserido até a raiz
        caminho.reverse()

        for i in range(len(caminho)):
            no = caminho[i]
            self.atualizar_altura(no)
            fator = self.obter_fator_balanceamento(no)

            # Se não tá desbalanceado, continua
            if fator <= 1 and fator >= -1:
                continue

            nova_sub_raiz = None

            # Caso LL (Left Left)
            if fator > 1 and valor < no.esquerda.valor:
                nova_sub_raiz = self.rotacao_direita(no)

            # Caso LR (Left Right)
            elif fator > 1 and valor > no.esquerda.valor:
                no.esquerda = self.rotacao_esquerda(no.esquerda)
                nova_sub_raiz = self.rotacao_direita(no)

            # Caso RR (Right Right)
            elif fator < -1 and valor > no.direita.valor:
                nova_sub_raiz = self.rotacao_esquerda(no)

            # Caso RL (Right Left)
            elif fator < -1 and valor < no.direita.valor:
                no.direita = self.rotacao_direita(no.direita)
                nova_sub_raiz = self.rotacao_esquerda(no)

            # Atualizar o ponteiro do pai ou a raiz
            if nova_sub_raiz is not None:
                if i == len(caminho) - 1:
                    # É a raiz
                    self.raiz = nova_sub_raiz
                else:
                    # Atualizar o ponteiro do pai
                    pai = caminho[i + 1]
                    if pai.esquerda == no:
                        pai.esquerda = nova_sub_raiz
                    else:
                        pai.direita = nova_sub_raiz

    def rotacao_direita(self, z: Node):
        y = z.esquerda

        if y is None:
            return z

        T3 = y.direita

        # Rotação
        y.direita = z
        z.esquerda = T3

        # Atualizar alturas
        self.atualizar_altura(z)
        self.atualizar_altura(y)

        return y

    def rotacao_esquerda(self, z: Node):
        y = z.direita

        if y is None:
            return z

        T2 = y.esquerda

        # Rotação
        y.esquerda = z
        z.direita = T2

        # Atualizar alturas
        self.atualizar_altura(z)
        self.atualizar_altura(y)

        return y

    def buscar(self, valor):
        no_atual = self.raiz

        if no_atual is None:
            return False

        while no_atual is not None:
            if valor == no_atual.valor:
                return True
            elif valor < no_atual.valor:
                no_atual = no_atual.esquerda
            else:
                no_atual = no_atual.direita

        return False

    def obter_altura(self, no: Node | None):
        if no:
            return no.altura
        return 0

    def atualizar_altura(self, no: Node):
        altura_esquerda = self.obter_altura(no.esquerda)
        altura_direita = self.obter_altura(no.direita)
        no.altura = 1 + max(altura_esquerda, altura_direita)

    def obter_fator_balanceamento(self, no: Node | None):
        if no is None:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def printar_arvore(self):
        if self.raiz is None:
            print("Árvore vazia!")
            return

        def obter_altura_no(no):
            if no is None:
                return 0
            return 1 + max(obter_altura_no(no.esquerda), obter_altura_no(no.direita))

        altura = obter_altura_no(self.raiz)
        largura = 2 ** altura - 1
        matriz = [[" " for _ in range(largura)] for _ in range(altura * 2)]

        def preencher_matriz(no, linha, esquerda, direita):
            if no is None:
                return

            meio = (esquerda + direita) // 2
            matriz[linha][meio] = str(no.valor)

            if no.esquerda:
                matriz[linha - 1][meio - 1] = "/"
                preencher_matriz(no.esquerda, linha - 2, esquerda, meio - 1)

            if no.direita:
                matriz[linha - 1][meio + 1] = "\\"
                preencher_matriz(no.direita, linha - 2, meio + 1, direita)

        preencher_matriz(self.raiz, len(matriz) - 1, 0, largura - 1)

        for i in range(len(matriz)):
            linha_str = "".join(matriz[i])
            if linha_str.strip():
                print(linha_str)
# Função para testar a estrutura da árvore
def arvore_teste(valores):
    print("== TESTE DE ARVORE ==")
    arvore = Arvore()
    # Inserir valores na Árvore
    inicio_arvore = time.perf_counter()
    for valor in valores:
        arvore.inserir(valor)
    print(f"tempo construção {time.perf_counter() - inicio_arvore:.6f}\n")


    # PRINTAR A ÁRVORE DE BAIXO PRA CIMA
    print("\n=== ESTRUTURA DA ÁRVORE ===")
    arvore.printar_arvore()
    print("=" * 30 + "\n")

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

