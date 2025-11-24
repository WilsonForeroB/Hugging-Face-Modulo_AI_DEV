# routes/file_routes.py
from fastapi import APIRouter
from schemas.sentimiento_schema import SentimientoInput
from schemas.tokenizar_schema import TokenizarInput
from services.Sentimiento_analisys import analisis_sentimiento
from services.Tokenizador import tokenizar_texto

router = APIRouter(
    prefix="/api/nlp",
    tags=["NLP"]
)

@router.post("/sentimiento_analisis")
async def sentimiento_analisis(payload: SentimientoInput):
    # Accedemos a los campos directamente
    user_id = payload.user_id
    texto = payload.texto_usuario

    # Pasamos el texto a tu función (ajusta si necesita user_id)
    resultado = analisis_sentimiento(texto)

    return {
        "user_id": user_id,
        "resultado": resultado
    }

@router.post("/tokenizar_texto")
async def tokenizar_texto_route(payload: TokenizarInput):
    # Accedemos a los campos directamente
    user_id = payload.user_id
    texto = payload.texto_usuario
    #print('texto usuario:', texto)
    # Pasamos el texto a tu función (ajusta si necesita user_id)
    resultado = tokenizar_texto(texto)

    return {
        "user_id": "wilson",
        "resultado": f"{resultado}" # pendiente de desarrollar para el lunes
    }
