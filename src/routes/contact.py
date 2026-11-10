from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(tags=["contacto"])

class Contacto(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=3, max_length=150)
    message: str = Field(min_length=10, max_length=1000)

@router.post("/contact", status_code=status.HTTP_201_CREATED)
async def crear_contacto(contacto: Contacto):
    # Próxima clase: acá se guarda en MySQL (tabla contactos)
    return {"ok": True, "mensaje": "Contacto recibido", "data": contacto}