import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from model import Modelo
from schemas import GestanteSchema, PredicaoSchema

app = FastAPI(
    title="API de Triagem de Risco Materno",
    version="1.0.0",
    description="Classifica gestantes como alto risco ou não, a partir de sinais vitais, com um modelo SVM embarcado.",
)
# shortcut: libera qualquer origem para o front-end abrir via file:// no MVP; em produção, restringir ao domínio do front-end.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST"], allow_headers=["*"])

modelo = Modelo()


@app.get("/", include_in_schema=False)
def documentacao():
    """Redireciona para a documentação Swagger."""
    return RedirectResponse(url="/docs")


@app.post("/predicao", response_model=PredicaoSchema, tags=["Predição"])
def predizer(gestante: GestanteSchema) -> PredicaoSchema:
    """Recebe os sinais vitais de uma gestante e retorna a classificação de risco. Os dados não são armazenados."""
    atributos = pd.DataFrame([gestante.para_atributos()])
    alto_risco = bool(modelo.realizar_predicao(atributos)[0])
    return PredicaoSchema(
        alto_risco=alto_risco,
        classificacao="Alto risco" if alto_risco else "Não alto risco",
    )
