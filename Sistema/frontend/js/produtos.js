let produtos = [];

checarSessao();
listarProdutos();

async function listarProdutos(busca = "") {
  const tbody = document.getElementById("lista-produtos");
  try {
    let url = `${API_URL}/estoque/itens`;
    if (busca) url += `?busca=${encodeURIComponent(busca)}`;

    const res = await fetch(url);
    produtos = await res.json();

    if (!produtos.length) {
      tbody.innerHTML = `<tr><td colspan="11" style="text-align:center;">Nenhum produto encontrado.</td></tr>`;
      return;
    }

    tbody.innerHTML = produtos.map(p => `
      <tr>
        <td>${p.id}</td>
        <td><strong>${p.nome}</strong></td>
        <td>${p.validade || "-"}</td>
        <td>${p.cor || "-"}</td>
        <td style="${p.alerta_minimo ? 'color: red; font-weight: bold;' : ''}">${p.quantidade}</td>
        <td>${p.unidade}</td>
        <td>
          <button class="btn-editar" onclick="editarProduto(${p.id})">Editar</button>
          <button class="btn-excluir" onclick="excluirProduto(${p.id})">Excluir</button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; color:red;">Erro ao carregar dados.</td></tr>`;
  }
}

function buscarProdutos() {
  const termo = document.getElementById("busca-nome").value.trim();
  listarProdutos(termo);
}

async function cadastrarProduto(){

  try {
        const itemData = {
            nome: document.getElementById("prod-nome").value,
            quantidade: document.getElementById("prod-qtd").value,
            unidade: document.getElementById("prod-unidade").value,
            validade: document.getElementById("prod-validade").value,
            cor: document.getElementById("prod-cor").value
        };
        const response = await fetch(`${API_URL}/estoque/itens`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(itemData)
        });
        if (!response.ok) {
            throw new Error('Erro na requisição');
        }
        const data = await response.json();
        console.log(data.message);
  } catch (error) {
      console.error('Erro ao cadastrar o item:', error);
  }
}

function limparBusca() {
  document.getElementById("busca-nome").value = "";
  listarProdutos();
}

function editarProduto(id) {
  const p = produtos.find(item => item.id === id);
  if (!p) return;

  fecharAviso("aviso-form");
  document.getElementById("titulo-form").textContent = "Editar Produto #" + p.id;
  document.getElementById("prod-id").value = p.id;
  document.getElementById("prod-nome").value = p.nome;
  document.getElementById("prod-validade").value = p.validade || "";
  document.getElementById("prod-cor").value = p.cor || "";
  document.getElementById("prod-textura").value = p.textura || "";
  document.getElementById("prod-peso").value = p.peso !== null ? p.peso : "";
  document.getElementById("prod-unidade").value = p.unidade;
  document.getElementById("prod-min").value = p.qt_minima;
  document.getElementById("prod-max").value = p.qt_maxima;

  document.getElementById("campo-qtd-inicial").style.display = "none";
  document.getElementById("btn-cancelar").style.display = "inline-block";
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetarFormulario() {
  document.getElementById("form-produto").reset();
  document.getElementById("prod-id").value = "";
  document.getElementById("titulo-form").textContent = "Novo Produto";
  document.getElementById("campo-qtd-inicial").style.display = "flex";
  document.getElementById("btn-cancelar").style.display = "none";
  fecharAviso("aviso-form");
}

document.getElementById("form-produto").addEventListener("submit", async (e) => {
  e.preventDefault();
  fecharAviso("aviso-form");
  fecharAviso("aviso-global");

  const id = document.getElementById("prod-id").value;
  const nome = document.getElementById("prod-nome").value.trim();
  const validade = document.getElementById("prod-validade").value || null;
  const cor = document.getElementById("prod-cor").value.trim() || null;
  const textura = document.getElementById("prod-textura").value.trim() || null;
  const peso = document.getElementById("prod-peso").value ? parseFloat(document.getElementById("prod-peso").value) : null;
  const unidade = document.getElementById("prod-unidade").value.trim() || "un";
  const qt_minima = parseFloat(document.getElementById("prod-min").value);
  const qt_maxima = parseFloat(document.getElementById("prod-max").value);

  if (!nome) {
    mostrarAviso("aviso-form", "O nome do produto é obrigatório.");
    return;
  }
  if (isNaN(qt_minima) || isNaN(qt_maxima) || qt_minima < 0 || qt_maxima < 0) {
    mostrarAviso("aviso-form", "Valores de estoque mínimo e máximo inválidos.");
    return;
  }
  if (qt_minima > qt_maxima) {
    mostrarAviso("aviso-form", "A quantidade mínima não pode ser maior que a máxima.");
    return;
  }

  const payload = { nome, validade, cor, textura, peso, qt_minima, qt_maxima, unidade };
  let url = `${API_URL}/estoque/itens`;
  let method = "POST";

  if (id) {
    url += `/${id}`;
    method = "PUT";
  } else {
    payload.quantidade = parseFloat(document.getElementById("prod-qtd").value) || 0;
  }

  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      mostrarAviso("aviso-form", data.detail || "Erro ao salvar.");
      return;
    }

    resetarFormulario();
    mostrarAviso("aviso-global", id ? "Produto atualizado com sucesso!" : "Produto cadastrado com sucesso!", true);
    listarProdutos();
  } catch (err) {
    mostrarAviso("aviso-form", "Erro ao conectar ao servidor.");
  }
});

async function excluirProduto(id) {
  if (!confirm("Deseja realmente excluir este produto?")) return;

  try {
    const res = await fetch(`${API_URL}/estoque/itens/${id}`, { method: "DELETE" });
    const data = await res.json();
    if (!res.ok) {
      mostrarAviso("aviso-global", data.detail || "Erro ao excluir.");
      return;
    }
    mostrarAviso("aviso-global", "Produto excluído com sucesso!", true);
    listarProdutos();
  } catch (err) {
    mostrarAviso("aviso-global", "Erro de conexão ao excluir.");
  }
}
