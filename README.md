# MVP — Triagem de Risco Materno

MVP da disciplina **Engenharia de Sistemas de Software Inteligentes** (Pós-graduação em Engenharia de Software — PUC-Rio).

Um modelo de Machine Learning classifica gestantes como **alto risco** ou **não alto risco** a partir de seis sinais
vitais de uma consulta de rotina. O modelo é servido de forma embarcada por uma API FastAPI e consumido por um
front-end em HTML, CSS e JavaScript.

- **Dataset:** [Maternal Health Risk — UCI](https://archive.ics.uci.edu/dataset/863/maternal+health+risk)
- **Notebook no Colab:** [abrir no Google Colab](https://colab.research.google.com/github/vtsouza29/mvp-maternal-health-risk/blob/main/notebook/MVP_Risco_Materno.ipynb)
- **Vídeo de apresentação:** _link do vídeo_

## Estrutura

```
├── data/                      # dataset original (lido pelo notebook via URL raw)
├── notebook/                  # notebook do Colab: análise, treino, avaliação e exportação
├── api/                       # back-end FastAPI com o modelo embarcado
│   ├── app.py                 # rotas da API
│   ├── model/                 # Carregador, Modelo e Avaliador (uma responsabilidade por classe)
│   ├── schemas/               # validação de entrada e formato da resposta
│   ├── ml_model/              # pipeline exportado pelo notebook (pickle)
│   └── tests/                 # testes PyTest + golden dataset
└── front/                     # formulário HTML/CSS/JS
```

## Como executar

Pré-requisito: Python 3.12.

```bash
cd api
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

A API sobe em http://127.0.0.1:8000 e a documentação Swagger fica em http://127.0.0.1:8000/docs.

Com a API rodando, abra o arquivo `front/index.html` no navegador, preencha os sinais vitais e clique em
**Classificar risco**.

## Testes

```bash
cd api
pytest
```

- `tests/test_modelo.py` — **teste de desempenho do modelo**. Calcula acurácia, recall e F1 da classe alto risco
  no golden dataset (o conjunto de teste do holdout, nunca visto no treino) e falha se alguma métrica ficar abaixo
  do limite definido.
- `tests/test_api.py` — verifica a rota de predição e a rejeição de valores fora das faixas fisiológicas.

### Substituindo o modelo

1. Execute o notebook e baixe `modelo_risco_materno.pkl` e `golden_dataset_teste.csv`.
2. Copie-os para `api/ml_model/` e `api/tests/data/`, respectivamente.
3. Rode `pytest`. **Se o teste de desempenho falhar, o novo modelo não deve ser implantado.**

> O pickle deve ser carregado com a mesma versão do scikit-learn usada no treino. Se o modelo for retreinado no
> Colab com outra versão, atualize `scikit-learn` em `api/requirements.txt` (o notebook imprime a versão usada).

## Segurança e privacidade

Dados de saúde são dados pessoais sensíveis (LGPD). A reflexão completa está na seção 13 do notebook. Na aplicação:
a API não armazena os dados enviados, coleta apenas os atributos necessários para a predição (sem nome ou
documento) e valida cada campo na entrada.
