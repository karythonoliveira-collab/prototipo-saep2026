from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from database import Base, engine

from services import services_movimentacao, services_produtos, services_usuario





Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Sistema de Controle de Estoque - SAEP",
    description="API com Python, FastAPI e SQLite",
    version="1.0.0"
)

app.include_router(services_usuario.router)
app.include_router(services_produtos.router)
app.include_router(services_movimentacao.router)

@app.get("/")
def home():
    return {
        "mensagem": "API SAEP funcionando",
        "status": "online"
    }