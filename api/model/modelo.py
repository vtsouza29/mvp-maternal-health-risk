import pickle
from pathlib import Path

import numpy as np
import pandas as pd

CAMINHO_MODELO_PADRAO = Path(__file__).resolve().parents[1] / "ml_model" / "modelo_risco_materno.pkl"
COLUNAS_ATRIBUTOS = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]


class Modelo:
    """Encapsula o pipeline de Machine Learning exportado pelo notebook."""

    def __init__(self, caminho: Path = CAMINHO_MODELO_PADRAO):
        # pickle executa código ao carregar: só carregamos o arquivo versionado no repositório, nunca um enviado por usuários.
        with open(caminho, "rb") as arquivo:
            self._pipeline = pickle.load(arquivo)

    def realizar_predicao(self, atributos: pd.DataFrame) -> np.ndarray:
        """Retorna 1 (alto risco) ou 0 (não alto risco) para cada linha recebida."""
        return self._pipeline.predict(atributos[COLUNAS_ATRIBUTOS])
