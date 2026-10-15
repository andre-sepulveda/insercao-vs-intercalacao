"""Testes que provam que os dois métodos ordenam corretamente.

Rodar com:  python testes.py
(usa só a biblioteca padrão, não precisa instalar nada)
"""

import random
import unittest

from ordenacao import (
    insercao,
    insercao_contando,
    intercalacao,
    intercalacao_contando,
)


# Cada função é testada da mesma forma. As versões "contando" devolvem uma
# tupla, então pegamos só a lista.
FUNCOES = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "insercao_contando": lambda v: insercao_contando(v)[0],
    "intercalacao_contando": lambda v: intercalacao_contando(v)[0],
}


class TestOrdenacao(unittest.TestCase):

    def verificar(self, entrada):
        """Confere todas as funções contra o sorted() do Python."""
        esperado = sorted(entrada)
        for nome, f in FUNCOES.items():
            with self.subTest(funcao=nome, entrada=entrada[:20]):
                original = list(entrada)
                self.assertEqual(f(entrada), esperado)
                # não pode alterar a lista recebida
                self.assertEqual(entrada, original)

    # --- casos difíceis exigidos ---------------------------------------
    def test_lista_vazia(self):
        self.verificar([])

    def test_um_elemento(self):
        self.verificar([42])

    def test_todos_iguais(self):
        self.verificar([7] * 50)

    def test_ja_ordenada(self):
        self.verificar(list(range(100)))

    def test_invertida(self):
        self.verificar(list(range(100, 0, -1)))

    # --- casos extras --------------------------------------------------
    def test_dois_elementos(self):
        self.verificar([2, 1])
        self.verificar([1, 2])

    def test_negativos_e_repetidos(self):
        self.verificar([3, -1, 0, -1, 3, 2, -5, 0])

    def test_floats(self):
        self.verificar([3.5, -0.25, 1e9, 0.0, 2.75])

    def test_strings(self):
        self.verificar(["pera", "abacaxi", "uva", "banana", "abacaxi"])

    def test_aleatorias(self):
        rng = random.Random(123)
        for n in [3, 10, 31, 64, 100, 257, 1000]:
            self.verificar([rng.randint(-1000, 1000) for _ in range(n)])

    def test_estabilidade(self):
        # pares (chave, posição original); compara só a chave
        class Item:
            def __init__(self, chave, pos):
                self.chave, self.pos = chave, pos

            def __lt__(self, outro):
                return self.chave < outro.chave

            def __gt__(self, outro):
                return self.chave > outro.chave

            def __le__(self, outro):
                return self.chave <= outro.chave

        rng = random.Random(7)
        itens = [Item(rng.randint(0, 5), i) for i in range(60)]
        for nome in ("insercao", "intercalacao"):
            with self.subTest(funcao=nome):
                saida = FUNCOES[nome](itens)
                for a, b in zip(saida, saida[1:]):
                    if a.chave == b.chave:
                        self.assertLess(a.pos, b.pos)


class TestComparacoes(unittest.TestCase):
    """Confere o contador com valores conhecidos da teoria."""

    def test_insercao_ordenada_faz_n_menos_1(self):
        n = 100
        _, c = insercao_contando(list(range(n)))
        self.assertEqual(c, n - 1)

    def test_insercao_invertida_faz_n_n_menos_1_sobre_2(self):
        n = 100
        _, c = insercao_contando(list(range(n, 0, -1)))
        self.assertEqual(c, n * (n - 1) // 2)

    def test_casos_triviais_sem_comparacao(self):
        self.assertEqual(insercao_contando([])[1], 0)
        self.assertEqual(insercao_contando([1])[1], 0)
        self.assertEqual(intercalacao_contando([])[1], 0)
        self.assertEqual(intercalacao_contando([1])[1], 0)

    def test_intercalacao_dentro_dos_limites(self):
        # Para n potência de 2: (n/2)*log2(n) <= comparações <= n*log2(n) - n + 1
        rng = random.Random(1)
        for k in range(1, 11):
            n = 2 ** k
            v = [rng.random() for _ in range(n)]
            _, c = intercalacao_contando(v)
            self.assertGreaterEqual(c, (n // 2) * k)
            self.assertLessEqual(c, n * k - n + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
