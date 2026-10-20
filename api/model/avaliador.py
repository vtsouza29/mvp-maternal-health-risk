import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from model.modelo import Modelo


class Avaliador:
    """Calcula as métricas de desempenho do modelo; a classe positiva (1) é alto risco."""

    def avaliar(self, modelo: Modelo, atributos: pd.DataFrame, classes_reais: pd.Series) -> dict[str, float]:
        predicoes = modelo.realizar_predicao(atributos)
        return {
            "acuracia": accuracy_score(classes_reais, predicoes),
            "precisao_alto_risco": precision_score(classes_reais, predicoes),
            "recall_alto_risco": recall_score(classes_reais, predicoes),
            "f1_alto_risco": f1_score(classes_reais, predicoes),
        }
