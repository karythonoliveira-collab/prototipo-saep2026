from fastapi import HTTPException, status
from sqlalchemy.orm import Session

#region user
class DuplicationUser(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="já existe um cliente com esse email",
        )

class NoteUser(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há cliente com esse id",
        )

class NoteAllUser(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há clientes no banco",
        )

class NoteUserSenha(HTTPException):
    def __init__(self, session: Session):
        session.rollback()

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há User Verificado com esse Email"
        )
#endregion

#region estoque
class DuplicationEstoque(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="já existe um produto com esse nome",
        )

class NoteEstoque(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há produto com esse id",
        )

class NoteAllEstoque(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há produtos no banco",
        )
#endregion

#region log
class NoteFoundLogs(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há log com esse id",
        )

#endregion

#region geral
class NoteAllLogs(HTTPException):
    def __init__(self, session: Session):
        session.rollback()
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há log no banco",
        )

class ErroInesperado(HTTPException):
    def __init__(self, e, session: Session | None = None):
        if session is not None:
            session.rollback()
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado do servidor. Erro -> {e}",
        )

class RequestInvalida(HTTPException):
    def __init__(self, session: Session | None = None):
        if session is not None:
            session.rollback()
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Nenhum campo devidamente informado",
        )

class VauleInvalido(HTTPException):
    def __init__(self, d: int, s: int, session: Session | None = None):
        if session is not None:
            session.rollback()
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Saída não permitida: estoque insuficiente. Disponível: {d}. Solicitado: {s}",
        )


#endregion

#region jwt
class JustAdmin(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail= "Essa opeção só pode ser excutada por admin."
        )

class JwtInvalido(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="JWT inválido"
        )
#endregion


