const API_URL = "http://127.0.0.1:8000";

function obterUsuario() {
  const u = sessionStorage.getItem("usuario");
  return u ? JSON.parse(u) : null;
}

function salvarUsuario(u) {
  sessionStorage.setItem("usuario", JSON.stringify(u));
}

function deslogar() {
  sessionStorage.removeItem("usuario");
  window.location.href = "login.html";
}

function checarSessao() {
  const u = obterUsuario();
  if (!u) {
    window.location.href = "login.html";
    return null;
  }
  const el = document.getElementById("usuario-nome");
  if (el) el.textContent = u.nome;
  return u;
}

function mostrarAviso(id, texto, sucesso = false) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = texto;
  el.className = sucesso ? "msg-sucesso" : "msg-erro";
  el.style.display = "block";
}

function fecharAviso(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.display = "none";
}
