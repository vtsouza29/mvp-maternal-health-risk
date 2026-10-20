from pathlib import Path

import pandas as pd


class Carregador:
    """Responsável apenas pela carga de dados tabulares."""

    def carregar_dados(self, caminho: str | Path) -> pd.DataFrame:
        """Lê um arquivo CSV (caminho local ou URL) e retorna um DataFrame."""
        return pd.read_csv(caminho)
