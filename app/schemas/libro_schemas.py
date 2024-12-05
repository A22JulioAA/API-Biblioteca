from pydantic import BaseModel
from datetime import datetime

from .genero_schemas import GeneroResponse

class LibroBase(BaseModel):
    isbn: str
    titulo: str
    autor: str
    descripcion: str
    editorial: str
    # Estos enteros son los IDs de los géneros
    generos: list[int]
    pais: str
    idioma: str
    num_paginas: int
    ano_edicion: int
    precio: float

class LibroCreate(LibroBase):
    isbn: str 
    titulo: str 
    autor: str 
    descripcion: str
    editorial: str 
    generos: list[int] 
    pais: str 
    idioma: str
    num_paginas: int
    ano_edicion: int 
    precio: float 

class LibroUpdate(LibroBase):
    titulo: str = None
    autor: str = None
    descripcion: str = None
    editorial: str = None
    generos: list[int] = None
    pais: str = None
    idioma: str = None
    num_paginas: int = None
    ano_edicion: int = None
    precio: float = None

class Libro(LibroBase):
    id: int

    class Config:
        from_attributes = True

class LibroResponse(LibroBase):
    id: int
    generos: list[GeneroResponse]

    class Config:
        from_attributes = True

class LibroInDB(LibroBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




