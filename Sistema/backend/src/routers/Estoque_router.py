from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database.db import get_connection
from schemas.User_schema import ItemCreateSchema, ItemUpdateSchema, MovimentacaoSchema

router = APIRouter(prefix="/estoque", tags=["Estoque"])

@router.get("/itens")
def listar_itens(busca: Optional[str] = Query(None), ordenar: Optional[str] = Query(None)):
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT i.id, i.nome, i.quantidade, i.validade, i.cor, i.unidade
            FROM Item i
        """
        params = []
        if busca and busca.strip():
            query += " WHERE i.nome LIKE ?"
            params.append(f"%{busca.strip()}%")

        cur.execute(query, params)
        rows = cur.fetchall()

        resultado = []
        for r in rows:
            qtd = float(r["quantidade"])
            resultado.append({
                "id": r["id"],
                "nome": r["nome"],
                "validade": r["validade"],
                "cor": r["cor"],
                "quantidade": qtd,
                "unidade": r["unidade"],
            })

        if ordenar == "alfabetica":
            resultado.sort(key=lambda x: str(x["nome"]).lower())

        return resultado
    finally:
        conn.close()

@router.get("/itens/{item_id}")
def obter_item(item_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT i.id, i.nome, i.quantidade, i.validade, i.cor, i.unidade
            FROM Item i
            WHERE i.id = ?
        """, (item_id,))
        r = cur.fetchone()
        qtd = float(r["quantidade"])
        if not r:
            raise HTTPException(status_code=404, detail="Item não encontrado.")
        return {
            "id": r["id"],
            "nome": r["nome"],
            "validade": r["validade"],
            "cor": r["cor"],
            "quantidade": qtd,
            "unidade": r["unidade"],
        }
    finally:
        conn.close()

@router.post("/itens")
def cadastrar_item(payload: ItemCreateSchema):
    if not payload.nome or not payload.nome.strip():
        raise HTTPException(status_code=400, detail="O nome do produto é obrigatório.")
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO Item (nome, quantidade, validade, cor, unidade)
               VALUES (?, ?, ?, ?, ?)""",
            (payload.nome.strip(), payload.quantidade, payload.validade, payload.cor,payload.unidade.strip() or "un")
        )
        conn.commit()
        item_id = cur.lastrowid
        return {"status": "success", "id": item_id, "message": "Produto cadastrado com sucesso!"}
    finally:
        conn.close()

@router.put("/itens/{item_id}")
def editar_item(item_id: int, payload: ItemUpdateSchema):
    if not payload.nome or not payload.nome.strip():
        raise HTTPException(status_code=400, detail="O nome do produto é obrigatório.")
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Item WHERE id = ?", (item_id,))
        item = cur.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado.")

        item_id = item["item_id"]

        cur.execute(
            """UPDATE Item SET nome = ?, validade = ?, cor = ?, textura = ?, peso = ?
               WHERE id = ?""",
            (payload.nome.strip(), payload.validade, payload.cor, payload.textura, payload.peso, item_id)
        )

        cur.execute(
            """UPDATE Estoque SET qt_minima = ?, qt_maxima = ?, unidade = ?
               WHERE id = ?""",
            (payload.unidade.strip() or "un", item_id)
        )

        conn.commit()
        return {"status": "success", "message": "Produto atualizado com sucesso!"}
    finally:
        conn.close()

@router.delete("/itens/{item_id}")
def excluir_item(item_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Item WHERE id = ?", (item_id,))
        item = cur.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado.")

        item_id = item["id"]
        cur.execute("DELETE FROM Item WHERE id = ?", (item_id,))
        if item_id:
            cur.execute("DELETE FROM Item WHERE id = ?", (item_id,))

        conn.commit()
        return {"status": "success", "message": "Produto excluído com sucesso!"}
    finally:
        conn.close()

@router.post("/movimentacao")
def registrar_movimentacao(payload: MovimentacaoSchema):
    if payload.quantidade <= 0:
        raise HTTPException(status_code=400, detail="A quantidade movimentada deve ser maior que zero.")
    if not payload.data or not payload.data.strip():
        raise HTTPException(status_code=400, detail="A data da movimentação é obrigatória.")

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT i.id, i.quantidade, i.unidade
            FROM Item i
            WHERE i.id = ?
        """, (payload.item_id,))
        item = cur.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado.")

        cur.execute("SELECT id FROM Usuario WHERE id = ?", (payload.usuario_id,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        qtd_atual = float(item["quantidade"])
        unidade = item["unidade"]
        tipo = payload.tipo.lower().strip()
        data_mov = payload.data.strip()

        if tipo == "entrada":
            nova_qtd = qtd_atual + payload.quantidade
            cur.execute(
                "INSERT INTO Log (usuario_id, item_id, dt, quantidade, tipo) VALUES (?, ?, ?, ?, ?)",
                (payload.usuario_id, payload.item_id, data_mov, payload.quantidade, "ENTRADA")
            )
        elif tipo == "saida":
            if qtd_atual < payload.quantidade:
                raise HTTPException(
                    status_code=400,
                    detail=f"Saldo insuficiente em estoque! Disponível: {qtd_atual} {unidade}"
                )
            nova_qtd = qtd_atual - payload.quantidade


            cur.execute(
                "INSERT INTO Log (usuario_id, item_id, dt, quantidade, tipo) VALUES (?, ?, ?, ?, ?)",
                (payload.usuario_id, payload.item_id, data_mov, payload.quantidade, 'SAIDA')
            )
        else:
            raise HTTPException(status_code=400, detail="Tipo de movimentação inválido. Use 'entrada' ou 'saida'.")

        cur.execute("UPDATE Item SET quantidade = ? WHERE id = ?", (nova_qtd, item["id"]))
        conn.commit()

        return {
            "status": "success",
            "produto": item["id"],
            "nova_quantidade": nova_qtd,
            "unidade": unidade,
            "mensagem_alerta": (
                f"ALERTA DE ESTOQUE CRÍTICO: O produto '{item['id']}' ficou com {nova_qtd} {unidade}, "
            )
        }
    finally:
        conn.close()

@router.get("/logs")
def listar_logs():
    conn = get_connection() 
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT l.id, l.dt, l.quantidade, l.tipo,
                   i.id as item_nome, u.id as usuario_nome
            FROM Log l
            LEFT JOIN Item i ON l.item_id = i.id
            LEFT JOIN Usuario u ON l.usuario_id = u.id
            ORDER BY l.id DESC
        """)
        rows = cur.fetchall()
        res = []
        for r in rows:
            res.append({
                "id": r["id"],
                "data": r["dt"],
                "operacao": "ENTRADA" if r["tipo"] == "ENTRADA" else "SAIDA",
                "quantidade": float(r["quantidade"]) if r["quantidade"] is not None else 0.0,
                "item_nome": r["item_nome"] or "Item Removido",
                "usuario_nome": r["usuario_nome"] or "Desconhecido"
            })
        return res
    finally:
        conn.close()
