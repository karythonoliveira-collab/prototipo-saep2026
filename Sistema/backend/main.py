import sys
import os

src_path = os.path.join(os.path.dirname(__file__), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from routers.User_router import router as user_router
from routers.Estoque_router import router as estoque_router

init_db()

app = FastAPI(title="SAEP - Sistema de Controle de Estoque")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(estoque_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
