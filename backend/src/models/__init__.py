from .estoque import Estoque
from .logs import Logs
from .usuario import Usuario

from ..db import Base, engine


__all__ = ["Estoque", "Logs", "Usuario"]


#criar todas as tabelas
Base.metadata.create_all(bind=engine)