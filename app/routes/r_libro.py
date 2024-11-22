# Rutas para la entidad Libro

from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.libro import Libro
from schemas.libro_schemas import LibroResponse

from database import get_db

libros_router = APIRouter(
    prefix='/libros',
    tags=['Libros']
)

@libros_router.get(
    '/',
    description='Obtener todos los libros',
    responses={
        200: {
            'description': 'Lista de libros',
            'model': LibroResponse
        },
        404: {
            'description': 'No hay libros registrados'
        }
    }
)
async def get_libros(db: Session = Depends(get_db)):
    libros = db.query(Libro).all()
    if libros:
        return libros
    raise HTTPException(status_code=404, detail='No hay libros registrados')