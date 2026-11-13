from sqlalchemy.orm import Session

from ..models import Log
from .erros import NoteAllEstoque, ErroInesperado

def read_all_logs(session: Session) -> dict:
    try:
        query = session.query(Log).all()

        if query is not None: raise NoteAllEstoque(session)

        dados: dict = {"mensagem": []}

        for i in query:
            dados["mensagem"].append({
                "id": i.id,
                "quem_fez": i.usuario.nome,
                "produdo": i.estoque.nome,
                "dt_caco": i.dt_acao,
                "is_retirada": bool(i.is_retirada)
            })
        
        return dados

    except NoteAllEstoque: raise

    except Exception as e:
        raise ErroInesperado(e, session)
