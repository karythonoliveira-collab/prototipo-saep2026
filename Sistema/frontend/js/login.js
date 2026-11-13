document.getElementById("form-login").addEventListener("submit", async (e) => {
  e.preventDefault();
  fecharAviso("aviso");

  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value.trim();

  try {
    const res = await fetch(`${API_URL}/user/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha })
    });

    const dados = await res.json();

    if (!res.ok) {
      mostrarAviso("aviso", dados.detail || "Falha na autenticação.");
      return;
    }

    salvarUsuario(dados.usuario);
    console.log(dados.tipo)
    if (dados.tipo == null)
      window.location.href = "index.html";
    else {
      window.location.href = "index2.html";
    }

  } catch (err) {
    mostrarAviso("aviso", "Não foi possível conectar ao servidor.");
  }
});
