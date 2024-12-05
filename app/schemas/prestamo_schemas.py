from pydantic import BaseModel
from datetime import date
from enum import Enum

class EstadoPrestamo(str, Enum):
    activo = 'activo'
    devuelto = 'devuelto'
    retrasado = 'retrasado'

class PrestamoBase(BaseModel):
    fecha_prestamo: date
    fecha_devolucion: date
    estado: EstadoPrestamo = EstadoPrestamo.activo

class PrestamoCreate(PrestamoBase):
    usuario_id: int
    libros_id: list[int]

class PrestamoUpdate(PrestamoBase):
    pass

class PrestamoResponse(PrestamoBase):
    id: int
    usuario_id: int
    libros_id: list[int]

    class Config:
        from_attributes = True

class Prestamo(PrestamoBase):
    pass

    
