from fastapi import FastAPI
from almoxarifado.routes import router as movimento_rota

app = FastAPI(title="API almoxarifado-SAEP", version="1.0.0")
app.include_router(movimento_rota)

@app.get("/")
def root():
    return {"message": "Api Rodando!"}
    