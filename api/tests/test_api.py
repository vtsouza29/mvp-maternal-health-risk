from fastapi.testclient import TestClient

from app import app

cliente = TestClient(app)

GESTANTE_ALTO_RISCO = {
    "idade": 35,
    "pressao_sistolica": 140,
    "pressao_diastolica": 95,
    "glicemia": 15.0,
    "temperatura": 98.0,
    "frequencia_cardiaca": 88,
}


def test_predicao_retorna_classificacao():
    resposta = cliente.post("/predicao", json=GESTANTE_ALTO_RISCO)

    assert resposta.status_code == 200
    assert resposta.json() == {"alto_risco": True, "classificacao": "Alto risco"}


def test_predicao_rejeita_valor_fora_da_faixa_fisiologica():
    resposta = cliente.post("/predicao", json={**GESTANTE_ALTO_RISCO, "frequencia_cardiaca": 7})

    assert resposta.status_code == 422
