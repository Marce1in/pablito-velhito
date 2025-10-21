# UniSenac Campus Pelotas  
## Senac Fecomércio Sesc  

---

### **Objetivo**
Compreender a lógica de balanceamento (rotações) numa **Árvore AVL**, implementada de forma iterativa (com laços) dentro da função **Inserir**.

---

### **Contexto**
Partimos do princípio que vocês já possuem uma **Árvore Binária de Busca (BST)** funcional em Python, com uma **Classe Node** e uma **Classe Árvore** (com funções `inserir` e `buscar` iterativas).

---

## **Parte 1: Modificações Essenciais**

A nossa **Classe Node** precisa de uma nova informação:

### 1. **Atributo altura:**
- No `__init__` da Classe Node, adicione `self.altura = 1`.  
  Todo novo nó, quando inserido como folha, tem altura 1.

---

### Precisaremos também de três “funções auxiliares” que o nosso algoritmo principal usará o tempo todo:

#### 1. **Função `obter_altura(no)`:**
- Recebe um nó.
- Se o nó for Nulo (`None`), ela deve retornar **0**.
- Caso contrário, ela retorna o atributo `no.altura`.

---

#### 2. **Função `atualizar_altura(no)`:**
- Recebe um nó.
- Esta função recalcula a altura de um nó com base nos seus filhos.
  ```python
  altura_esquerda = obter_altura(no.filho_esquerda)
  altura_direita  = obter_altura(no.filho_direita)
  no.altura = 1 + max(altura_esquerda, altura_direita)
  ```

---

#### 3. **Função `obter_fator_balanceamento(no)`:**
- Recebe um nó.
- Se o nó for Nulo, retorna **0**.
- Calcula:
  ```python
  obter_altura(no.filho_esquerda) - obter_altura(no.filho_direita)
  ```
- O resultado (fator) ideal é **-1, 0 ou 1**.  
  - Se for > 1 → a árvore está “pesada” para a esquerda.  
  - Se for < -1 → está “pesada” para a direita.

---

## **Parte 2: O Algoritmo Inserir da AVL (Iterativo)**

Este algoritmo é dividido em duas grandes fases:
- **(A)** a inserção normal da BST, mas “gravando o caminho”;
- **(B)** a “subida” de volta para a raiz, verificando o balanceamento.

---

### **Fase A: Inserção Normal (BST) + Rastreamento do Caminho**

O desafio de não usar recursão é que, após descer até uma folha para inserir, precisamos “subir” de volta para a raiz.  
Para fazer isso, vamos usar uma lista para “gravar” cada nó visitado no caminho da raiz até o local de inserção.

---

#### **Passos:**

1. **Crie o novo_nó**
   ```python
   novo_no = Node(valor_para_inserir, altura = 1)
   ```

2. **Crie uma lista (ou pilha) chamada `caminho`**

3. **Tratar Árvore Vazia:**
   - Se a raiz da árvore for Nula, atribua o `novo_no` à raiz e termine a função.

4. **Encontrar o Local:**
   - Comece com um ponteiro `atual` na raiz.
   - Inicie um laço (`while True`):
     - **IMPORTANTE:** Adicione o nó atual à lista `caminho`.
     - Compare o `valor_para_inserir` com `atual.valor`.

---

#### **Caso Menor:**
- Se `atual.filho_esquerda` for Nulo:
  - Atribua o `novo_no` como `atual.filho_esquerda`.
  - Termine o laço (`break`).
- Se não for Nulo:
  - Mova o ponteiro atual para `atual.filho_esquerda`.

---

#### **Caso Maior:**
- Se `atual.filho_direita` for Nulo:
  - Atribua o `novo_no` como `atual.filho_direita`.
  - Termine o laço (`break`).
- Se não for Nulo:
  - Mova o ponteiro atual para `atual.filho_direita`.

---

> **Ao fim desta fase**, o `novo_no` foi inserido e a lista `caminho` contém todos os ancestrais dele, da raiz até o seu pai.

---

### **Fase B: Verificação de Balanceamento (Subida)**

Agora, verificaremos o balanceamento da árvore na “subida” para frente (do pai do `novo_no` até a raiz).

1. **Inicie um loop** que percorre a lista `caminho` em ordem reversa.  
   Para cada nó do caminho (ancestral):

2. **Passo A: Atualizar Altura**
   - Sempre que visitarmos um nó, a primeira coisa a fazer é atualizar sua altura:
     ```python
     atualizar_altura(no_ancestral)
     ```

3. **Passo B: Verificar Balanceamento**
   - Calcule o fator de balanceamento:
     ```python
     fator = obter_fator_balanceamento(no_ancestral)
     ```

4. **Passo C: Detectar Desequilíbrio**
   - Se o fator for maior que 1 ou menor que -1, identificamos um nó desbalanceado.
   - Precisamos verificar se é o caso:
     - **LL**, **RR**, **LR**, ou **RL**.

---

#### **Casos:**

- **Se o valor inserido for menor que o valor do filho da esquerda (LL):**  
  - Execute a **rotação à direita**.

- **Se o valor inserido for maior que o valor do filho da esquerda (LR):**  
  - Execute a **rotação dupla esquerda-direita**.

- **Se o valor inserido for maior que o valor do filho da direita (RR):**  
  - Execute a **rotação à esquerda**.

- **Se o valor inserido for menor que o valor do filho da direita (RL):**  
  - Execute a **rotação dupla direita-esquerda**.

---

## **Parte 3: Algoritmos das Rotações**

Estes são os algoritmos detalhados para as rotações (simples) que irá precisar.

---

### **Lógica: Rotação Simples à Direita (para o caso LL)**

1. **Função chamada como:** `nova_raiz = rotacao_direita(z)`  
   Onde `z` é o nó desbalanceado.

2. **Identifique:**  
   - Filho esquerdo de `z` (chame-o de `y`).
   - Filho direito de `y` (chame-o de `T3`, subárvore que mudará de posição).

3. **Executar Rotações:**  
   ```python
   y.filho_direita = z
   z.filho_esquerda = T3
   ```

4. **Atualizar Alturas (A ORDEM IMPORTA!):**
   ```python
   atualizar_altura(z)
   atualizar_altura(y)
   ```

5. **Retorne `y` (nova raiz da subárvore, usada no passo D1)**

---

### **Lógica: Rotação Simples à Esquerda (para o caso RR)**

1. **Função chamada como:** `nova_raiz = rotacao_esquerda(z)`  
   Onde `z` é o nó desbalanceado.

2. **Identifique:**  
   - Filho direito de `z` (chame-o de `y`).
   - Filho esquerdo de `y` (chame-o de `T2`, subárvore que mudará de posição).

3. **Executar Rotações:**  
   ```python
   y.filho_esquerda = z
   z.filho_direita = T2
   ```

4. **Atualizar Alturas (A ORDEM IMPORTA!):**
   ```python
   atualizar_altura(z)
   atualizar_altura(y)
   ```

5. **Retorne `y` (nova raiz da subárvore, usada no passo D1)**

---

### **Rotações Duplas**

- **Rotação Dupla Esquerda-Direita (LR):**
  1. Faça uma **rotação à esquerda** no filho esquerdo do nó desbalanceado.
  2. Faça uma **rotação à direita** no nó desbalanceado.

- **Rotação Dupla Direita-Esquerda (RL):**
  1. Faça uma **rotação à direita** no filho direito do nó desbalanceado.
  2. Faça uma **rotação à esquerda** no nó desbalanceado.

---

### **Passo Final: Reconectar Sub-Árvore Após Rotação**

1. Uma vez que encontrou qual nó “subiu” após a rotação, você precisa atualizar o ponteiro do ancestral (pai) correspondente.
2. Verifique se o ancestral estava à esquerda ou à direita do pai anterior e substitua.
3. Se o nó rotacionado era a raiz, atualize o atributo principal da árvore (`self.raiz`).

---

### **Pergunta Ativa**
Como poderíamos garantir que, após uma rotação, toda a árvore se mantém balanceada de forma iterativa, sem precisar “subir” novamente para atualizar alturas?

---

**Fim do Documento**
