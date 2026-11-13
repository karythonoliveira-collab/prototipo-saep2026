from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models import Usuario
from .erros import DuplicationUser, NoteUser, RequestInvalida, NoteAllUser, ErroInesperado, NoteUserSenha
from .jwt import criar_token

#region CRUD

def create_user(nome: str, senha: str, email: str, is_admin: bool ,session : Session) -> dict:
    try:
        user = Usuario(nome, email, senha, is_admin)

        session.add(user)
        session.commit()
        return {'mensagem': 'cliente criado com sucesso'}
    
    except IntegrityError:
        raise DuplicationUser(session)
    
    except Exception as e:
        raise ErroInesperado(e, session)

def dellet_user(id: int, session: Session) -> dict:
    try:

        query = session.query(Usuario).filter_by(id = id).delete() 

        if query:
            session.commit()
            return {"mensagem": "cliente removido."}
        else: raise NoteUser(session)

    #relançar o erro 
    except (NoteUser) : raise

    except Exception as e:
        raise ErroInesperado(e, session)

def update_user(id: int, senha: str  | None, nome: str | None, session: Session) -> dict:
    try:
        query = session.query(Usuario).filter_by(id = id).first()

        if query:
            if senha != None :  query.nova_senha(senha)  
             
            if nome != None: query.nome = nome 

            if nome is None and senha is None: raise RequestInvalida(session)

        else: raise NoteUser(session)

        session.commit()
        return {'mensagem': 'cliente editado com sucesso.'}

    except (NoteUser, RequestInvalida) : raise

    except Exception as e:
        raise ErroInesperado(e, session)

def read_user(id: int, session: Session) -> dict:
    try:
        query = session.query(Usuario).filter_by(id = id).first()

        if query is not None:
            return {
                'mensagem':{
                    'nome' : query.nome,
                    'email' : query.email,
                    'is_admin': query.is_admin
                }
            }
        else: raise NoteUser(session)
    
    except (NoteUser): raise

    except Exception as e:
        raise ErroInesperado(e, session)   

def read_all_user(session: Session) -> dict:
    try:
        query = session.query(Usuario).all()

        dados : dict = {"mensagem": []}

        if query is not None: raise NoteAllUser(session)

        for i in query:
            dados['mensagem'].append({
                'id': i.id,
                'nome' : i.nome,
                'email' : i.email,
                'is_admin': i.is_admin
            })
            
    except (NoteAllUser): raise

    except Exception as e:
        raise ErroInesperado(e, session)  

#endregion

def login_user(email: str, senha: str, session: Session) -> dict:
    try:    
        query = session.query(Usuario).filter_by(email = email).first()  # type: ignore


        if query is None: raise NoteUserSenha(session)

        if query.verificarSenha(senha) and query.is_admin == 1:  
            jwt = criar_token(query.id, is_admin= True)
        
        elif query.verificarSenha(senha): 
            jwt = criar_token(query.id)

        else: raise NoteUserSenha(session)

        return {
                "access_token": jwt,
                "token_type": "bearer"
            }

    except (NoteUserSenha): raise

    except Exception as e:
        raise ErroInesperado(e, session)

