from pydantic import BaseModel
from datetime import date, datetime

class AutorBase(BaseModel):
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    fecha_fallecimiento: date
    nacionalidad: str
    biografia: str
    imagen: str

class AutorCreate(AutorBase):
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    fecha_fallecimiento: date = None
    nacionalidad: str
    biografia: str
    imagen: str = None

class AutorUpdate(AutorBase):
    nombre: str = None
    apellidos: str = None
    fecha_nacimiento: date = None
    fecha_fallecimiento: date = None
    nacionalidad: str = None
    biografia: str = None
    imagen: str = None

class Autor(AutorBase):
    id: int

    class Config:
        from_attributes = True

class AutorBasicResponse(BaseModel):
    nombre: str
    apellidos: str

    class Config:
        from_attributes = True

class AutorResponse(AutorBase):
    id: int

    class Config:
        from_attributes = True

class AutorLibroResponse(BaseModel):
    nombre: str

    class Config:
        from_attributes = True

class AutorInDB(AutorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True