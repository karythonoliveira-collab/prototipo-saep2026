from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Produto
from schemas.schemas_produto import ProdutoCreate

router = APIRouter(prefix =  "/produto")

@router.post("/cadastro_produto")
def cadastrar_produto(
        dados:ProdutoCreate,
        usuario_id: int,
        db:Session = Depends(get_db)
):
    produto = Produto(
        nome = dados.nome,
        quantidade = dados.quantidade,
        preco = dados.preco,
        usuario_id = usuario_id
    )
    db.add(produto)
    db.commit()
    db.refresh(produto) 

    return produto

@router.get("/Listar_produtos")
def listar_produtos(
        usuario_id:int,
        admin:bool = False,
        db:Session = Depends(get_db)
    ):

    consulta= db.query(Produto)

    if not admin:
        consulta = consulta.filter(Produto.usuario_id == usuario_id)

    total = consulta.count()

    produtos = (consulta.order_by(Produto.id))

    return{
        "total": total,
        "produtos": produtos
    }

@router.get("/buscar_produtos")
def buscar_produtos(
        produto_id:int,
        usuario_id:int,
        admin: bool = False,
        db:Session = Depends(get_db)
):
    produto = db.get(Produto, produto_id)
    if produto is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail="Produto não encontrado"
        )
    if not admin and produto_id.usuario_id != usuario_id:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
        detail="Você não tem permissão para acessar esses produtos"
        )
    return produto  

@router.patch("/atualizar_produtos")
def atualizar_produto(
        produto_id:int,
        dados: ProdutoCreate,
        usuario_id:int,
        admin: bool = False,
        db:Session = Depends(get_db)
):
    produto = buscar_produtos(
        db, produto_id, usuario_id, admin
    )
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade

    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/Deletar_produtos")
def excluir_produto(
        produto_id: int,
        usuario_id: int,
        admin: bool = False,
        db:Session = Depends(get_db)
):
    produto = buscar_produtos(
        db, produto_id, usuario_id, admin
    )

    db.delete(produto)
    db.commit()
    return None