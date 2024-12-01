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
    genero: list[int]
    pais: str
    idioma: str
    num_paginas: int
    ano_edicion: int
    precio: float

class LibroCreate(LibroBase):
    isbn: str = "9906453786057"
    titulo: str = "El señor de los anillos"
    autor: str = "J.R.R. Tolkien"
    descripcion: str = "Un anillo para gobernarlos a todos, un anillo para encontrarlos, un anillo para atraerlos a todos y atarlos en las tinieblas."
    editorial: str = "Minotauro"
    genero: list[int] = [1, 2]
    pais: str = "Reino Unido"
    idioma: str = "Español"
    num_paginas: int = 1216
    ano_edicion: int = 1954
    precio: float = 25.95

class LibroUpdate(LibroBase):
    pass

class Libro(LibroBase):
    id: int

    class Config:
        orm_mode = True

class LibroResponse(LibroBase):
    id: int
    genero: list[GeneroResponse]

    class Config:
        orm_mode = True

class LibroInDB(LibroBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True




