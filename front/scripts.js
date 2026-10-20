const URL_API = "http://127.0.0.1:8000/predicao";

const formulario = document.getElementById("formulario-gestante");
const resultado = document.getElementById("resultado");
const botao = formulario.querySelector("button");

const exibirResultado = (titulo, mensagem, classe) => {
  resultado.className = `resultado ${classe}`;
  const elementoTitulo = document.createElement("h2");
  elementoTitulo.textContent = titulo;
  const elementoMensagem = document.createElement("p");
  elementoMensagem.textContent = mensagem;
  resultado.replaceChildren(elementoTitulo, elementoMensagem);
  resultado.hidden = false;
};

const lerGestante = () => {
  const dados = new FormData(formulario);
  return Object.fromEntries([...dados].map(([campo, valor]) => [campo, Number(valor)]));
};

const solicitarPredicao = async (gestante) => {
  const resposta = await fetch(URL_API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(gestante),
  });
  if (!resposta.ok) {
    throw new Error("A API recusou os dados. Confira se os valores estão nas faixas indicadas.");
  }
  return resposta.json();
};

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  if (!formulario.reportValidity()) {
    return;
  }

  botao.disabled = true;
  try {
    const predicao = await solicitarPredicao(lerGestante());
    if (predicao.alto_risco) {
      exibirResultado(predicao.classificacao, "Priorizar acompanhamento pré-natal especializado.", "alto-risco");
    } else {
      exibirResultado(predicao.classificacao, "Manter o acompanhamento pré-natal de rotina.", "sem-risco");
    }
  } catch (erro) {
    const mensagem = erro instanceof TypeError
      ? "Não foi possível conectar à API. Verifique se o back-end está rodando."
      : erro.message;
    exibirResultado("Erro", mensagem, "");
  } finally {
    botao.disabled = false;
  }
});
