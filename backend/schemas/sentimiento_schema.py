from pydantic import BaseModel

class SentimientoInput(BaseModel):
    user_id: str
    texto_usuario: str
