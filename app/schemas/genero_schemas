from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GeneroBase(BaseModel):
    nombre: str
    descripcion: str = None
    
class GeneroCreate(GeneroBase):
    pass

class GeneroUpdate(GeneroBase):
    pass

class Genero(GeneroBase):
    id: int
    
    class Config:
        orm_mode = True

class GeneroResponse(GeneroBase):
    id: int

    class Config:
        orm_mode = True

class GeneroInDB(GeneroBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True