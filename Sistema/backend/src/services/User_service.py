from sqlalchemy.orm import Session
from schemas.User_schema import criar_user_schema as cus
from models.User_db import Usuario

def criar_user(db: Session, data:cus): 

    user = Usuario(
        nome = data.nome,
        email = data.email,
        senha = data.senha
    )

    db.add(user)
    db.flush()
    db.commit()
    db.refresh(user)
