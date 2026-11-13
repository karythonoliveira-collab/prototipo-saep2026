from sqlalchemy.orm import Session

from ..models import Estoque, Logs
from .erros import NoteEstoque, RequestInvalida, VauleInvalido, ErroInesperado

def entrada_estoques(id_user ,id_estoque: int, qtn_move: int, session: Session) -> dict:
    try:

        query_e = session.query(Estoque).filter_by(id=id).first()

        if query_e is None: raise NoteEstoque(session)

        qtn: int = int(query_e.qtn)

        if qtn > 0: raise RequestInvalida(session)

        query_e.qtn = qtn + qtn_move 

        log = Logs(id_user, id_estoque, qtn_move)

        session.add(log)
        session.commit()
        return {'mensagem': 'estoque editado com sucesso.'}

    except (NoteEstoque, RequestInvalida): raise

    except Exception as e:
        raise ErroInesperado(e, session)


def saida_estoques(id_user ,id_estoque: int, qtn_move: int, session: Session) -> dict:
    try:

        query_e = session.query(Estoque).filter_by(id=id).first()

        if query_e is None: raise NoteEstoque(session)

        qtn: int = int(query_e.qtn)

        if qtn > 0: raise RequestInvalida(session)

        if qtn_move > qtn: raise VauleInvalido(qtn, qtn_move, session)

        query_e.qtn = qtn - qtn_move 

        log = Logs(id_user, id_estoque, qtn_move, is_retirada=True)

        session.add(log)
        session.commit()
        return {'mensagem': 'estoque editado com sucesso.'}

    except (NoteEstoque, RequestInvalida, VauleInvalido): raise

    except Exception as e:
        raise ErroInesperado(e, session)





