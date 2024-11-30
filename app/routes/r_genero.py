# Rutas para la entidad Género

# Importamos las librerías necesarias
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Importamos el logger
from log_config import setup_logger

# Importamos los modelos y esquemas necesarios
from models.genero import Genero
from schemas.genero_schemas import GeneroResponse, GeneroCreate

# Importamos la función para obtener la base de datos
from database import get_db

# Creamos el router para los libros
generos_router = APIRouter(
    prefix='/generos',
    tags=['Géneros']
)

# Configuramos el logger
user_logger, internal_logger = setup_logger()

# Ruta para obtener todos los géneros
@generos_router.get(
    '/',
    description='Obtener todos los géneros',
    responses={
        200: {
            'description': 'Lista de géneros',
            'model': GeneroResponse
        },
        404: {
            'description': 'No hay géneros registrados'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def get_libros(db: Session = Depends(get_db)):
    try: 
        # Consultamos los géneros de la base de datos. Si no hay géneros, se lanza una excepción
        generos = db.query(Genero).all()

        # Si hay géneros, los devolvemos. Si no, lanzamos una excepción
        if generos:
            return generos
        else:
            raise HTTPException(status_code=404, detail='No hay géneros registrados')
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))