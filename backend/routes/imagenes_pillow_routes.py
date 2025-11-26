from fastapi import APIRouter
from pydantic import BaseModel
from services.imagenes_pillow_service import procesar_imagen_servicio_pillow

router = APIRouter(
    prefix="/api/imagenes_pillow",
    tags=["Imagenes Pillow"]
)

class ImagenInput(BaseModel):
    user_id: str
    path_imagen: str
    conversation_id: str

#http://127.0.0.1:7000 prefix:/api/imagenes_pillow/ function: procesar_imagen_pillow

@router.post("/procesar_imagen_pillow")
async def procesar_imagen_pillow(payload: ImagenInput):
    
    resultado = procesar_imagen_servicio_pillow()

    return {
        "user_id": 'wilson',
        "imagenes": resultado
    }