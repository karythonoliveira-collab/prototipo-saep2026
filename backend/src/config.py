from os import getenv 
from dotenv import load_dotenv

load_dotenv()

DB_URL = getenv("DB_URL")
SECRETES_KEY = getenv("SECRETES_KEY")

ALG = 'HS256'

#Em minutos
TIMER = 5
