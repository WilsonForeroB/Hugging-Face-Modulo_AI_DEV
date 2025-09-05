from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Sentimiento_analisys import analisis_sentimiento
from Tokenizador import tokenizar_texto

huggface = FastAPI(title="huggingface_modul")

# habilitar CORS (ajusta en producción)
huggface.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diccionario de funciones disponibles
FUNCTIONS = {
    "sentiment": analisis_sentimiento,
    "tokenizar": tokenizar_texto,
}

@huggface.get("/")
def root():
    return {"status": "ok", "functions": list(FUNCTIONS.keys())}

@huggface.post("/run")
def run(function: str, text: str):
    if function not in FUNCTIONS:
        raise HTTPException(status_code=400, detail=f"Función no soportada: {function}")
    fn = FUNCTIONS[function]
    try:
        result = fn(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"function": function, "result": result}

if __name__ == "__main__":
    uvicorn.run(
        "main:huggface",
        host="0.0.0.0",
        port=6000,
        reload=True
    )