# Ordenação por inserção × intercalação

Trabalho em dupla: implementação e comparação experimental da ordenação por inserção e da ordenação por intercalação (merge sort), com o `sorted()` do Python como referência.

**Dupla:** Andre Sepulveda e _[nome da dupla]_

## Arquivos

| arquivo | o que é |
|---|---|
| `ordenacao.py` | os dois métodos (com e sem contador de comparações) |
| `testes.py` | testes que provam que ordenam certo |
| `medir.py` | roda tudo e gera o CSV e os gráficos |
| `dados.csv` | os números brutos das medições |
| `grafico_tempo.png` / `grafico_comparacoes.png` | os gráficos |
| `RELATORIO.md` | a análise |

## Como rodar

Precisa de **Python 3.8 ou mais novo**. A única dependência externa é o `matplotlib`, usado só para os gráficos:

```bash
pip install -r requirements.txt
```

(No Windows, se `pip` não for reconhecido, use `py -m pip install -r requirements.txt`.)

### Rodar os testes

```bash
python testes.py
```

Os testes usam só a biblioteca padrão (`unittest`). Cobrem lista vazia, um elemento, todos iguais, já ordenada, invertida, além de negativos, floats, strings, listas aleatórias, estabilidade e a contagem de comparações nos casos com resposta conhecida (lista ordenada faz n−1, invertida faz n(n−1)/2).

### Refazer as medições e os gráficos

```bash
python medir.py
```

Esse comando apaga e recria do zero `dados.csv`, `grafico_tempo.png` e `grafico_comparacoes.png`, e imprime no terminal as tabelas de médias e o ponto de virada. Leva poucos segundos.

Pode ser rodado de qualquer pasta, porque os arquivos são sempre gravados ao lado do `medir.py`.

## Formato do `dados.csv`

Uma linha por algoritmo × tamanho × repetição (3 × 10 × 30 = 900 linhas):

| coluna | significado |
|---|---|
| `algoritmo` | `insercao`, `intercalacao` ou `sorted` |
| `n` | tamanho da lista |
| `repeticao` | 1 a 30 |
| `tempo_s` | tempo daquela execução, em segundos |
| `comparacoes` | comparações feitas (vazio para `sorted`, que é em C) |

Na mesma repetição, os três algoritmos ordenam **a mesma lista**.

## Configurações

No topo do `medir.py`:

- `TAMANHOS`: os valores de n;
- `REPETICOES = 30`: o enunciado pede no mínimo 10;
- `SEMENTE = 2026`: semente fixa, para as listas (e portanto as comparações) serem sempre as mesmas.
