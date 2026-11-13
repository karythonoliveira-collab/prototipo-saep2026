from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from ..models import Estoque
from .erros import DuplicationEstoque, NoteEstoque, RequestInvalida, NoteAllEstoque, ErroInesperado


#region CRUD
def create_estoque(nome: str, preco_uni: float, qtn: int, session : Session) -> dict:
    try:

        estoque = Estoque(nome, preco_uni, qtn,datetime.now())

        session.add(estoque)
        session.commit()
        return {'mensagem': 'estoque criado com sucesso'}
    
    except IntegrityError:
        raise DuplicationEstoque(session)
    
    except Exception as e:
        raise ErroInesperado(e, session)

def update_estoque(id: int, session : Session, nome: str | None = None, preco_uni: int| None = None, qtn: int | None = None):

    try:
        query = session.query(Estoque).filter_by(id = id).first()

        if query:
            if nome != None: query.nome = nome

            if preco_uni != None: query.preco_uni = preco_uni

            if qtn != None: query.qtn = qtn

            #verifique se nada foi prenchido
            if nome is None and preco_uni is None and qtn is None: 
                raise RequestInvalida(session)
        
        else: 
            raise NoteEstoque(session)

        session.commit()
        return {'mensagem': 'estoque editado com sucesso.'}

    except (NoteEstoque, RequestInvalida) : raise
    
    except Exception as e:
        raise ErroInesperado(e, session)

def dellet_estoque(id: int, session: Session) -> dict:
    try:

        query = session.query(Estoque).filter_by(id = id).delete() 

        if query:
            session.commit()
            return {"mensagem": "estoque removido."}
        else: raise NoteEstoque(session)

    #relançar o erro 
    except (NoteEstoque) : raise

    except Exception as e:
        raise ErroInesperado(e, session)   

def read_estoque(id: int, session: Session) -> dict:
    try:
        query = session.query(Estoque).filter_by(id=id).first()

        if query is not None:
            return {
                "mensagem": {
                    "id": query.id,
                    "nome": query.nome,
                    "preco_uni": query.preco_uni,
                    "qtn": query.qtn,
                    "dt_cads": query.dt_cads,
                }
            }
        else: raise NoteEstoque(session)

    except NoteEstoque: raise

    except Exception as e:
        raise ErroInesperado(e, session)

def read_all_estoque(session: Session) -> dict:
    try:
        query = session.query(Estoque).order_by(Estoque.nome).all()

        if query is not None: raise NoteAllEstoque(session)

        dados: dict = {"mensagem": []}

        for i in query:
            dados["mensagem"].append({
                "id": i.id,
                "nome": i.nome,
                "dt_cads": i.dt_cads
            })
        
        return dados

    except NoteAllEstoque: raise

    except Exception as e:
        raise ErroInesperado(e, session)
#endregion


def read_estoque_nome(nome: str, session: Session) -> dict:
    try:
        query = session.query(Estoque).filter_by(nome=nome).first()

        if query is not None:
            return {
                "mensagem": {
                    "id": query.id,
                    "nome": query.nome,
                    "preco_uni": query.preco_uni,
                    "qtn": query.qtn,
                    "dt_cads": query.dt_cads,
                }
            }
        else: raise NoteEstoque(session)

    except NoteEstoque: raise

    except Exception as e:
        raise ErroInesperado(e, session)


