from dotenv import load_dotenv
import os
import json

archivo_configuracion = ".env" 

load_dotenv(archivo_configuracion)

TOKEN_HUGFACE = os.getenv("TOKEN_HUGFACE")
MODELO_BASE=os.getenv("MODELO_BASE")