"""Ordenação por inserção e ordenação por intercalação (merge sort).

Cada algoritmo tem duas versões:

- ``insercao`` / ``intercalacao``: versão "limpa", usada para medir o tempo.
- ``insercao_contando`` / ``intercalacao_contando``: mesma lógica, mas conta
  quantas comparações entre elementos foram feitas. Fica separada para que o
  contador não pese na medição de tempo.

Todas as funções devolvem uma lista NOVA e não alteram a lista recebida.
"""


# ---------------------------------------------------------------------------
# Ordenação por inserção
# ---------------------------------------------------------------------------

def insercao(lista):
    """Ordena por inserção e devolve uma nova lista ordenada."""
    v = list(lista)
    for i in range(1, len(v)):
        chave = v[i]
        j = i - 1
        # desloca para a direita os elementos maiores que a chave
        while j >= 0 and v[j] > chave:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = chave
    return v


def insercao_contando(lista):
    """Igual a ``insercao``, mas devolve ``(lista_ordenada, comparacoes)``."""
    v = list(lista)
    comparacoes = 0
    for i in range(1, len(v)):
        chave = v[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1          # comparação v[j] > chave
            if v[j] > chave:
                v[j + 1] = v[j]
                j -= 1
            else:
                break
        v[j + 1] = chave
    return v, comparacoes


# ---------------------------------------------------------------------------
# Ordenação por intercalação (merge sort)
# ---------------------------------------------------------------------------

def _intercalar(esq, dir):
    """Junta duas listas já ordenadas em uma só (estável)."""
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:          # <= mantém a ordenação estável
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado


def intercalacao(lista):
    """Ordena por intercalação e devolve uma nova lista ordenada."""
    if len(lista) <= 1:
        return list(lista)
    meio = len(lista) // 2
    return _intercalar(intercalacao(lista[:meio]), intercalacao(lista[meio:]))


def _intercalar_contando(esq, dir):
    resultado = []
    i = j = 0
    comparacoes = 0
    while i < len(esq) and j < len(dir):
        comparacoes += 1              # comparação esq[i] <= dir[j]
        if esq[i] <= dir[j]:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir[j:])
    return resultado, comparacoes


def intercalacao_contando(lista):
    """Igual a ``intercalacao``, mas devolve ``(lista_ordenada, comparacoes)``."""
    if len(lista) <= 1:
        return list(lista), 0
    meio = len(lista) // 2
    esq, c_esq = intercalacao_contando(lista[:meio])
    dir, c_dir = intercalacao_contando(lista[meio:])
    resultado, c_meio = _intercalar_contando(esq, dir)
    return resultado, c_esq + c_dir + c_meio
