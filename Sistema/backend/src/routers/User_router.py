from fastapi import APIRouter, HTTPException
from database.db import get_connection
from schemas.User_schema import UserLoginSchema, UserCreateSchema, UserResponseSchema

router = APIRouter(prefix="/user", tags=["Usuario"])

@router.post("/login")
def login(payload: UserLoginSchema):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nome, email, senha, administrador FROM Usuario WHERE email = ?", (payload.email.strip(),))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado.")
        if user["senha"] != payload.senha.strip():
            raise HTTPException(status_code=401, detail="Senha incorreta.")

        return {
            "status": "success",
            "usuario": {
                "id": user["id"],
                "nome": user["nome"],
                "email": user["email"],
                "tipo": user["administrador"]
            }
        }
    finally:
        conn.close()

@router.post("/criar", response_model=UserResponseSchema)
def criar(payload: UserCreateSchema):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM Usuario WHERE email = ?", (payload.email.strip(),))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

        cur.execute(
            "INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)",
            (payload.nome.strip(), payload.email.strip(), payload.senha.strip())
        )
        conn.commit()
        novo_id = cur.lastrowid
        return {"id": novo_id, "nome": payload.nome.strip(), "email": payload.email.strip()}
    finally:
        conn.close()

@router.get("/listar")
def listar():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nome, email FROM Usuario")
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
