"""Roda todas as medições e gera dados.csv, grafico_tempo.png e
grafico_comparacoes.png do zero.

Uso:  python medir.py

Para cada n, gera REPETICOES listas aleatórias. Cada lista é ordenada pelos
três métodos (inserção, intercalação, sorted). Assim os três sempre ordenam
exatamente as mesmas entradas.
"""

import csv
import random
import time
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")  # gera os PNG sem precisar abrir janela
import matplotlib.pyplot as plt

from ordenacao import (
    insercao,
    insercao_contando,
    intercalacao,
    intercalacao_contando,
)

TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 30          # o enunciado pede no mínimo 10
SEMENTE = 2026           # semente fixa: as listas são as mesmas a cada execução

PASTA = Path(__file__).resolve().parent
ARQ_CSV = PASTA / "dados.csv"
ARQ_TEMPO = PASTA / "grafico_tempo.png"
ARQ_COMP = PASTA / "grafico_comparacoes.png"

ALGORITMOS = {
    "insercao": insercao,
    "intercalacao": intercalacao,
    "sorted": sorted,
}
CONTADORES = {
    "insercao": insercao_contando,
    "intercalacao": intercalacao_contando,
}


def cronometrar(funcao, lista):
    """Tempo, em segundos, de uma chamada de ``funcao(lista)``."""
    inicio = time.perf_counter()
    funcao(lista)
    return time.perf_counter() - inicio


def medir():
    """Devolve a lista de linhas brutas (uma por algoritmo x n x repetição)."""
    rng = random.Random(SEMENTE)
    linhas = []
    for n in TAMANHOS:
        for rep in range(1, REPETICOES + 1):
            lista = [rng.randint(0, 10 * n) for _ in range(n)]
            esperado = sorted(lista)
            for nome, funcao in ALGORITMOS.items():
                tempo = cronometrar(funcao, lista)
                if nome in CONTADORES:
                    saida, comps = CONTADORES[nome](lista)
                    assert saida == esperado, f"{nome} ordenou errado (n={n})"
                else:
                    comps = ""  # sorted() é em C, não dá para contar
                linhas.append({
                    "algoritmo": nome,
                    "n": n,
                    "repeticao": rep,
                    "tempo_s": f"{tempo:.9f}",
                    "comparacoes": comps,
                })
        print(f"  n = {n:>4} ok")
    return linhas


def salvar_csv(linhas):
    with open(ARQ_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, fieldnames=["algoritmo", "n", "repeticao", "tempo_s", "comparacoes"]
        )
        w.writeheader()
        w.writerows(linhas)


def medias(linhas):
    """{algoritmo: {n: (tempo_medio_s, comparacoes_medias ou None)}}"""
    resumo = {}
    for nome in ALGORITMOS:
        resumo[nome] = {}
        for n in TAMANHOS:
            grupo = [l for l in linhas if l["algoritmo"] == nome and l["n"] == n]
            t = mean(float(l["tempo_s"]) for l in grupo)
            c = None
            if nome in CONTADORES:
                c = mean(int(l["comparacoes"]) for l in grupo)
            resumo[nome][n] = (t, c)
    return resumo


def ponto_de_virada(a, b):
    """Menor n a partir do qual b < a em TODOS os tamanhos seguintes.

    ``a`` e ``b`` são dicionários {n: valor}. Devolve None se não houver.
    """
    for i, n in enumerate(TAMANHOS):
        if all(b[m] < a[m] for m in TAMANHOS[i:]):
            return n
    return None


def grafico(series, titulo, rotulo_y, arquivo):
    fig, ax = plt.subplots(figsize=(8, 5))
    estilos = {
        "insercao": ("Inserção", "o-", "#d1495b"),
        "intercalacao": ("Intercalação", "s-", "#2e86ab"),
        "sorted": ("sorted() do Python", "^--", "#6c757d"),
    }
    for nome, valores in series.items():
        rotulo, marcador, cor = estilos[nome]
        ax.plot(TAMANHOS, [valores[n] for n in TAMANHOS], marcador,
                label=rotulo, color=cor, linewidth=2, markersize=5)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(TAMANHOS)
    ax.set_xticklabels([str(n) for n in TAMANHOS])
    ax.minorticks_off()
    ax.set_xlabel("Tamanho da lista (n) - escala log")
    ax.set_ylabel(rotulo_y + " - escala log")
    ax.set_title(titulo)
    ax.grid(True, which="major", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(arquivo, dpi=120)
    plt.close(fig)


def main():
    # apaga resultados antigos para garantir que tudo é refeito do zero
    for arq in (ARQ_CSV, ARQ_TEMPO, ARQ_COMP):
        if arq.exists():
            arq.unlink()

    print(f"Medindo {len(TAMANHOS)} tamanhos x {REPETICOES} repeticoes...")
    linhas = medir()
    salvar_csv(linhas)
    resumo = medias(linhas)

    tempo_us = {nome: {n: resumo[nome][n][0] * 1e6 for n in TAMANHOS}
                for nome in ALGORITMOS}
    comps = {nome: {n: resumo[nome][n][1] for n in TAMANHOS}
             for nome in CONTADORES}

    grafico(tempo_us, "Tempo médio de ordenação", "Tempo (microssegundos)", ARQ_TEMPO)
    grafico(comps, "Número médio de comparações", "Comparações", ARQ_COMP)

    # tabelas em Markdown, prontas para colar no relatório
    print("\nTempo medio (microssegundos)\n")
    print("| n | Insercao | Intercalacao | sorted() |")
    print("|---:|---:|---:|---:|")
    for n in TAMANHOS:
        print(f"| {n} | {tempo_us['insercao'][n]:.2f} | "
              f"{tempo_us['intercalacao'][n]:.2f} | {tempo_us['sorted'][n]:.2f} |")

    print("\nComparacoes medias\n")
    print("| n | Insercao | Intercalacao |")
    print("|---:|---:|---:|")
    for n in TAMANHOS:
        print(f"| {n} | {comps['insercao'][n]:.1f} | {comps['intercalacao'][n]:.1f} |")

    vt = ponto_de_virada(tempo_us["insercao"], tempo_us["intercalacao"])
    vc = ponto_de_virada(comps["insercao"], comps["intercalacao"])
    print(f"\nIntercalacao passa a ser mais rapida a partir de n = {vt}")
    print(f"Intercalacao passa a fazer menos comparacoes a partir de n = {vc}")
    print(f"\nGerados: {ARQ_CSV.name}, {ARQ_TEMPO.name}, {ARQ_COMP.name}")


if __name__ == "__main__":
    main()
