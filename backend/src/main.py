from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import manger_route as mr

app = FastAPI(title="Api do Almoxarifado", 
              description="Almoxarifado de uma empresa de médio porte no seto de materias de limpeza",
              redoc_url=None, 
              contact={
                "name": "Arthur Nunes De Carvalho",
                "url": "https://github.com/NunesDevelloper",
                "email": "arthurnunescarvalho2@gmail.com",
            }
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(mr)