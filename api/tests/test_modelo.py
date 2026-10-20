"""Teste de desempenho do modelo: barra a implantação de um modelo que não atenda aos requisitos.

Para substituir o modelo, troque o arquivo em ml_model/ e rode `pytest`. Se algum teste falhar, o novo modelo não
deve ser implantado. As métricas são calculadas sobre o golden dataset: o conjunto de teste do holdout, exportado
pelo notebook e nunca visto pelo modelo durante o treino.
"""

from pathlib import Path

import pytest

from model import Avaliador, Carregador, Modelo

CAMINHO_GOLDEN_DATASET = Path(__file__).resolve().parent / "data" / "golden_dataset_teste.csv"
COLUNA_ALVO = "HighRisk"

# Requisitos de desempenho (classe positiva = alto risco). Modelo atual no golden dataset:
#   acurácia 0,879 | precisão 0,773 | recall 0,739 | F1 0,756
# Com 23 casos de alto risco no golden dataset, cada erro move o recall em ~4 p.p.; os limites têm folga para isso.

# Bem acima dos 0,75 de um modelo trivial que sempre responde "não alto risco".
LIMIAR_ACURACIA = 0.80
# Requisito principal da triagem: identificar ao menos 7 em cada 10 gestantes de alto risco.
LIMIAR_RECALL_ALTO_RISCO = 0.70
# Impede que o recall seja obtido sinalizando quase todas as gestantes (precisão muito baixa).
LIMIAR_F1_ALTO_RISCO = 0.70


@pytest.fixture(scope="module")
def metricas() -> dict[str, float]:
    golden_dataset = Carregador().carregar_dados(CAMINHO_GOLDEN_DATASET)
    atributos = golden_dataset.drop(columns=COLUNA_ALVO)
    classes_reais = golden_dataset[COLUNA_ALVO]
    return Avaliador().avaliar(Modelo(), atributos, classes_reais)


def test_acuracia_minima(metricas):
    assert metricas["acuracia"] >= LIMIAR_ACURACIA


def test_recall_minimo_alto_risco(metricas):
    assert metricas["recall_alto_risco"] >= LIMIAR_RECALL_ALTO_RISCO


def test_f1_minimo_alto_risco(metricas):
    assert metricas["f1_alto_risco"] >= LIMIAR_F1_ALTO_RISCO
