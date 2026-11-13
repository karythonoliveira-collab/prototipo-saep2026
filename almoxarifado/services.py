from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import MovimentacaoModel, ProdutoModel, UsuarioModel, UsuarioModel
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse, ProdutoCreate, ProdutoResponse, ProdutoUpdate, MovimentacaoCreate, MovimentacaoResponse


class UserService:

    @staticmethod
    def create(db: Session, user_in: UsuarioCreate) -> UsuarioModel:
        existe = (
            db.query(UsuarioModel).filter(UsuarioModel.email == user_in.email).first()

        )
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado.",

            )

        db_user = UsuarioModel(
            nome=user_in.nome,
            email=user_in.email,
            senha=user_in.senha,
            perfil=user_in.perfil,

        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update(db: Session, user_id: int, user_in: UsuarioUpdate) -> UsuarioModel:
        db_user = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado" 
                
            )
        update_data = user_in.model_dump(exclude_unset=True)

        if "email" in update_data:
            email_exist = (
                db.query(UsuarioModel)
                .filter(
                    UsuarioModel.email == update_data["email"],
                    UsuarioModel.id_user != user_id,
                ).first()
            )
            if email_exist:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este e-mail já está em uso por outro usuário.",
                )

        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user

class ProdutoService:

    @staticmethod
    def create(db: Session, produto_in: ProdutoCreate) -> ProdutoModel:
        db_produto = ProdutoModel(
            nome=produto_in.nome,
            quantidade_estoque=produto_in.quantidade_estoque,
            valor_uni=produto_in.valor_uni,
        
        )
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
        return db_produto
    @staticmethod
    def get_all(db: Session, nome: str | None = None):
        query = db.query(ProdutoModel)
        if nome:
            query = query.filter(ProdutoModel.nome.ilike(f"%{nome}%"))
        return query,all()

    @staticmethod
    def update(
        db: Session, produto_id: int, produto_in: ProdutoUpdate) -> ProdutoModel:
        db_produto = db.query(ProdutoModel).filter(ProdutoModel.id_usuario == produto_id).first()
        if not db_produto:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, detail="Produto não encontrado" \
                
            )
        update_data = produto_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_produto, key, value)

        db.commit()
        db.refresh(db_produto)
        return db_produto

    
class MovimentoService:
    @staticmethod
    def create(db: Session, movement_in: MovimentacaoCreate) -> MovimentacaoModel:
        tipo_upper = movement_in.tipo.upper

        if tipo_upper not in ("ENTRADA", "SAIDA"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo inválido. Use 'ENTRADA' ou 'SAIDA'.",
            )
        produto = (
            db.query(ProdutoModel)
            .filter(ProdutoModel.id_produto == movement_in.id_produto)
            .first()
        )
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado!"

            )
        user = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == movement_in.id_user).first()
        if not user:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado" \
                
            )

        if tipo_upper == "SAIDA":
            if produto.quantidade_estoque < movement_in.quantidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(f"saida não permitida: estoque insuficiente. disponível:"
                            f" {produto.quantidade_estoque}. Solicitado:"
                            f" {movement_in.quantidade}"
                            )
                    )
            produto.quantidade_estoque -= movement_in.quantidade
        else:
            produto.quantidade_estoque += movement_in.quantidade

        db_movement = MovimentacaoModel(
            tipo=tipo_upper,
            quantidade=movement_in.quantidade,
            id_produto=movement_in.id_produto,
            datetime_movimentacao=datetime.now(),
            id_user=movement_in.id_user,
        )

        db.add(db_movement)
        db.commit()
        db.refresh(db_movement)
        db.refresh(produto)

        return db_movement

    @staticmethod
    def get_all(db: Session):
        return db.query(MovimentacaoModel).all()
    