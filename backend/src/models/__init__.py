from .estoque import Estoque
from .log import Log
from .usuario import Usuario

from ..db import Base, engine


__all__ = ["Estoque", "Log", "Usuario"]


#criar todas as tabelas
Base.metadata.create_all(bind=engine)