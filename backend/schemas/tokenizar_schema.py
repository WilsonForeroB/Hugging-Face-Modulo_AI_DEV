from pydantic import BaseModel

class TokenizarInput(BaseModel):
    user_id: str
    model: str
    texto_usuario: str