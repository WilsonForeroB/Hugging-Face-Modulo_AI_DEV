# routes/imagenes_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.imagenes_opencv import procesar_imagen_local

router = APIRouter(
    prefix="/api/imagenes",
    tags=["Imagenes OpenCV"]
)


class ImagenInput(BaseModel):
    user_id: str
    path_imagen: str


@router.post("/procesar-local")
async def procesar_imagen_local_route(payload: ImagenInput):
    
    resultado = procesar_imagen_local(payload.path_imagen)

    return {
        "user_id": payload.user_id,
        "imagenes": resultado
    }
