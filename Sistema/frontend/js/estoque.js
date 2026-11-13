let usuarioAtual = checarSessao();
let produtosEstoque = [];

document.getElementById("data-movimentacao").value = new Date().toISOString().split("T")[0];

carregarDados();

function ordenarAlfabeticamente(lista) {
  if (lista.length <= 1) return lista;
  const pivo = lista[Math.floor(lista.length / 2)];
  const pivoNome = pivo.nome.toLowerCase();

  const menores = [];
  const iguais = [];
  const maiores = [];

  for (let item of lista) {
    const nome = item.nome.toLowerCase();
    if (nome < pivoNome) menores.push(item);
    else if (nome > pivoNome) maiores.push(item);
    else iguais.push(item);
  }

  return [...ordenarAlfabeticamente(menores), ...iguais, ...ordenarAlfabeticamente(maiores)];
}

async function carregarDados() {
  await carregarProdutos();
  await carregarLogs();
}

async function carregarProdutos() {
  const tbody = document.getElementById("lista-estoque");
  const select = document.getElementById("select-produto");

  try {
    const res = await fetch(`${API_URL}/estoque/itens`);
    const dados = await res.json();
    produtosEstoque = ordenarAlfabeticamente(dados);

    select.innerHTML = '<option value="">-- Selecione o produto --</option>' +
      produtosEstoque.map(p => `<option value="${p.id}">${p.nome} (Saldo: ${p.quantidade} ${p.unidade})</option>`).join("");

    if (!produtosEstoque.length) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;">Nenhum item cadastrado.</td></tr>`;
      return;
    }

    tbody.innerHTML = produtosEstoque.map(p => {
      let status = "Normal";
      let estilo = "";
      if (p.quantidade < p.qt_minima) {
        status = "Abaixo do Mínimo";
        estilo = "color: red; font-weight: bold;";
      } else if (p.quantidade > p.qt_maxima) {
        status = "Acima do Máximo";
        estilo = "color: orange;";
      }

      return `
        <tr>
          <td>${p.id}</td>
          <td><strong>${p.nome}</strong></td>
          <td style="${estilo}"><strong>${p.quantidade}</strong></td>
          <td>${p.qt_minima}</td>
          <td>${p.qt_maxima}</td>
          <td>${p.unidade}</td>
          <td style="${estilo}">${status}</td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:red;">Erro ao carregar dados.</td></tr>`;
  }
}

document.getElementById("form-movimentacao").addEventListener("submit", async (e) => {
  e.preventDefault();
  fecharAviso("alerta-critico");
  fecharAviso("aviso-movimentacao");

  const itemId = parseInt(document.getElementById("select-produto").value);
  const tipo = document.getElementById("tipo-movimentacao").value;
  const quantidade = parseFloat(document.getElementById("qtd-movimentacao").value);
  const data = document.getElementById("data-movimentacao").value;

  if (!itemId) {
    mostrarAviso("alerta-critico", "Selecione um produto.");
    return;
  }
  if (!quantidade || quantidade <= 0) {
    mostrarAviso("alerta-critico", "Informe uma quantidade válida.");
    return;
  }
  if (!data) {
    mostrarAviso("alerta-critico", "Informe a data da movimentação.");
    return;
  }

  const payload = {
    usuario_id: usuarioAtual.id,
    item_id: itemId,
    tipo: tipo,
    quantidade: quantidade,
    data: data
  };

  try {
    const res = await fetch(`${API_URL}/estoque/movimentacao`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const resposta = await res.json();

    if (!res.ok) {
      mostrarAviso("alerta-critico", resposta.detail || "Erro ao registrar movimentação.");
      return;
    }

    mostrarAviso("aviso-movimentacao", `Movimentação de ${tipo.toUpperCase()} realizada com sucesso!`, true);

    if (resposta.alerta_minimo && resposta.mensagem_alerta) {
      mostrarAviso("alerta-critico", resposta.mensagem_alerta);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    document.getElementById("qtd-movimentacao").value = "";
    carregarDados();
  } catch (err) {
    mostrarAviso("alerta-critico", "Erro ao conectar com a API.");
  }
});

async function carregarLogs() {
  const tbody = document.getElementById("lista-logs");
  try {
    const res = await fetch(`${API_URL}/estoque/logs`);
    const logs = await res.json();

    if (!logs.length) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;">Nenhuma movimentação registrada.</td></tr>`;
      return;
    }

    tbody.innerHTML = logs.map(l => `
      <tr>
        <td>${l.id}</td>
        <td>${l.dt}</td>
        <td><strong>${l.tipo}</strong></td>
        <td>${l.quantidade}</td>
        <td>${l.item_id}</td>
        <td>${l.usuario_id}</td>
      </tr>
    `
  ).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:red;">Erro ao carregar histórico.</td></tr>`;
  }
}
