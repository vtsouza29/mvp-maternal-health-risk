from pydantic import BaseModel, Field


class GestanteSchema(BaseModel):
    """Sinais vitais de uma consulta. As faixas rejeitam valores fisiologicamente implausíveis."""

    idade: int = Field(ge=10, le=70, description="Idade em anos", examples=[35])
    pressao_sistolica: int = Field(ge=60, le=200, description="Pressão sistólica em mmHg", examples=[140])
    pressao_diastolica: int = Field(ge=30, le=140, description="Pressão diastólica em mmHg", examples=[95])
    glicemia: float = Field(ge=1, le=30, description="Glicemia em mmol/L", examples=[15.0])
    temperatura: float = Field(ge=95, le=107, description="Temperatura corporal em °F", examples=[98.0])
    frequencia_cardiaca: int = Field(ge=40, le=200, description="Frequência cardíaca em bpm", examples=[88])

    def para_atributos(self) -> dict[str, float]:
        """Converte os campos da API para os nomes de colunas usados no treino do modelo."""
        return {
            "Age": self.idade,
            "SystolicBP": self.pressao_sistolica,
            "DiastolicBP": self.pressao_diastolica,
            "BS": self.glicemia,
            "BodyTemp": self.temperatura,
            "HeartRate": self.frequencia_cardiaca,
        }


class PredicaoSchema(BaseModel):
    """Resultado da triagem retornado ao front-end."""

    alto_risco: bool
    classificacao: str
