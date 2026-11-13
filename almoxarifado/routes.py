from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import (
    MovimentacaoCreate,
    MovimentacaoResponse,
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioCreate
)
from database import get_db
from services import UsuarioService, MovimentoService, ProdutoService
router = APIRouter()



@router.post(
    "/Usuarios",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuarios"],
)
def create_Usuario(Usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
  return UsuarioService.create(db, Usuario_in)


@router.get("/Usuarios", response_model=list[UsuarioResponse], tags=["Usuarios"])
def list_Usuarios(db: Session = Depends(get_db)):
  return UsuarioService.get_all(db)


@router.patch("/Usuarios/{Usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"])
def update_Usuario(
    Usuario_id: int, Usuario_in: UsuarioUpdate, db: Session = Depends(get_db)
):
  return UsuarioService.update(db, Usuario_id, Usuario_in)



@router.post(
    "/produtos",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Produtos"],
)
def create_Produto(Produto_in: ProdutoCreate, db: Session = Depends(get_db)):
  return ProdutoService.create(db, Produto_in)


@router.get("/produtos", response_model=list[ProdutoResponse], tags=["Produtos"])
def list_Produtos(nome: str | None = None, db: Session = Depends(get_db)):
 
  return ProdutoService.get_all(db, nome=nome)


@router.patch(
    "/produtos/{Produto_id}", response_model=ProdutoResponse, tags=["Produtos"]
)
def update_Produto(
    Produto_id: int, Produto_in: ProdutoUpdate, db: Session = Depends(get_db)
):
  return ProdutoService.update(db, Produto_id, Produto_in)



@router.post(
    "/movimentacoes",
    response_model=MovimentacaoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Movimentações"],
)
def create_Movimentacao(Movimentacao_in: MovimentacaoCreate, db: Session = Depends(get_db)):
  return MovimentoService.create(db, Movimentacao_in)


@router.get(
    "/movimentacoes", response_model=list[MovimentacaoResponse], tags=["Movimentações"]
)
def list_Movimentacaos(db: Session = Depends(get_db)):
  return MovimentoService.get_all(db)
