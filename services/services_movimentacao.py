from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from models import Movimentacao, Produto
from schemas.schemas_movimentacao import MovimentaçãoRegistro

router = APIRouter(prefix =  "/movimentação")

@router.post("/saída")
def registro_saida(
        usuario_id: int,
        db:Session = Depends(get_db)

):  
    if Movimentacao.quantidade > Produto.quantidade:
        Movimentacao.quantidade = Movimentacao.quantidade - Produto.quantidade
    else:
        print("A quantidade de saída é maior que a quantidade que tem no estoque!!")

    saida = db.post(Movimentacao)

    db.commit()
    db.refresh(saida)
    return saida


@router.post("/entrada")
def registro_entrada(
        dados:MovimentaçãoRegistro,
        usuario_id:int,
        db:Session = Depends(get_db)
):
    entrada =  Movimentacao(
        tipo = dados.tipo,
        quantidade = dados.quantidade,
        valor = dados.valor,
        id_produto = dados.id_produto,
        usuario_id = usuario_id,
        data = dados.data
    )
    db.add(entrada)
    db.commit()
    db.refresh(entrada)
    return entrada