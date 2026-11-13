from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from schemas.schemas_usuario import UsuarioCreate

router = APIRouter(prefix =  "/Usuario")

@router.post("/cadastro_usuario")
def cadastrar_Usuario(
        dados:UsuarioCreate,
        db:Session = Depends(get_db)
):
    usuario= Usuario(
        nome = dados.nome,
        admin = dados.admin
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario

@router.get("/Listar_usuarios")
def listar_usuario(
        db:Session = Depends(get_db)
):
   listagem =  db.query(Usuario)

   lista = listagem.count()

   return{
       "lista": lista
   }

@router.get("/Buscar_usuarios")
def buscar_usuarios(
        usuario_id:int,
        admin: bool = False,
        db:Session = Depends(get_db)
):
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail="Usuário não encontrado"
        )
    if not admin and usuario_id.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
        detail="Você não tem permissão para acessar esses usuários"
        )
    return usuario

@router.patch("/Atualizar_usuario")
def atualizar_usuario(
        usuario_id: int,
        dados: UsuarioCreate,
        admin: bool = False,
        db:Session = Depends(get_db)
):
    usuario = buscar_usuarios(
        db, usuario_id, admin
    )
    usuario.nome = dados.nome

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/Deletar_Usuario")
def excluir_usuario( 
        usuario_usuario_id: int,
        admin: bool = False,
        db:Session = Depends(get_db)
):
    usuario = buscar_usuarios(
        db, usuario_usuario_id, admin
    )

    db.delete(usuario)
    db.commit()
    return None
