from pydantic import BaseModel

class LibroBase(BaseModel):
    isbn: str
    titulo: str
    autor: str
    descripcion: str
    editorial: str
    genero: str
    pais: str
    idioma: str
    num_paginas: int
    ano_edicion: int
    precio: float

class LibroCreate(LibroBase):
    pass

class LibroUpdate(LibroBase):
    pass

class Libro(LibroBase):
    id: int

    class Config:
        orm_mode = True

class LibroResponse(LibroBase):
    id: int

    class Config:
        orm_mode = True

class LibroInDB(LibroBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True




