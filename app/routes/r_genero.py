# Rutas para la entidad Género

# Importamos las librerías necesarias
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Path
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
    response_model=list[GeneroResponse],
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
        internal_logger.error(f'Error al obtener los géneros: {str(e)}')
        raise HTTPException(status_code=500, detail='Error obteniendo los géneros')
    
# Ruta para obtener un género por su ID
@generos_router.get(
    '/{genero_id}',
    description='Obtener un género por su ID',
    response_model=GeneroResponse,
    responses={
        200: {
            'description': 'Género encontrado',
            'model': GeneroResponse
        },
        404: {
            'description': 'Género no encontrado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def get_genero(genero_id: int = Path(..., ge=1, description='ID del género'), db: Session = Depends(get_db)):
    try:
        # Consultamos el género por su ID. Si no existe, lanzamos una excepción
        genero = db.query(Genero).filter(Genero.id == genero_id).first()

        # Si el género existe, lo devolvemos. Si no, lanzamos una excepción
        if genero:
            return genero
        else:
            raise HTTPException(status_code=404, detail='Género no encontrado')
        
    except SQLAlchemyError as e:
        internal_logger.error(f'Error al obtener el género: {str(e)}')
        raise HTTPException(status_code=500, detail='Error obteniendo el género')
    
# Ruta para crear un género
@generos_router.post(
    '/',
    description='Crear un género',
    response_model=GeneroResponse,
    responses={
        201: {
            'description': 'Género creado',
            'model': GeneroResponse
        },
        400: {
            'description': 'Datos inválidos'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def create_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    try:
        # Normalizamos el nombre del género
        genero.nombre = genero.nombre.lower()

        if db.query(Genero).filter(Genero.nombre == genero.nombre).first():
            raise HTTPException(status_code=400, detail='El género ya existe')

        # Creamos el género en la base de datos
        nuevo_genero = Genero(**genero.dict(), created_at=datetime.now(), updated_at=datetime.now())
        db.add(nuevo_genero)
        db.commit()
        db.refresh(nuevo_genero)

        user_logger.info(f'Género creado: {nuevo_genero.id}')
        
        return nuevo_genero
        
    except SQLAlchemyError as e:
        internal_logger.error(f'Error al crear el género: {str(e)}')
        raise HTTPException(status_code=500, detail='Error creando el género')
    
# Ruta para actualizar un género
@generos_router.put(
    '/{genero_id}',
    description='Actualizar un género',
    response_model=GeneroResponse,
    responses={
        200: {
            'description': 'Género actualizado',
            'model': GeneroResponse
        },
        400: {
            'description': 'Datos inválidos'
        },
        404: {
            'description': 'Género no encontrado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def update_genero(genero: GeneroCreate,genero_id: int = Path(..., ge=1, description='ID del género'), db: Session = Depends(get_db)):
    try:
        # Consultamos el género por su ID. Si no existe, lanzamos una excepción
        genero_db = db.query(Genero).filter(Genero.id == genero_id).first()

        # Si el género existe, lo actualizamos. Si no, lanzamos una excepción
        if genero_db:
            if genero.nombre:
                genero_db.nombre = genero.nombre.lower()
            if genero.descripcion:
                genero_db.descripcion = genero.descripcion

            genero_db.updated_at = datetime.now()

            db.commit()
            db.refresh(genero_db)

            user_logger.info(f'Género actualizado: {genero_db.id}')
            
            return genero_db
        else:
            raise HTTPException(status_code=404, detail='Género no encontrado')
        
    except SQLAlchemyError as e:
        internal_logger.error(f'Error al actualizar el género: {str(e)}')
        raise HTTPException(status_code=500, detail='Error actualizando el género')
    
# Ruta para eliminar un género
@generos_router.delete(
    '/{genero_id}',
    description='Eliminar un género',
    response_model=GeneroResponse,
    responses={
        204: {
            'description': 'Género eliminado'
        },
        404: {
            'description': 'Género no encontrado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def delete_genero(genero_id: int = Path(..., ge=1, description='ID del género'), db: Session = Depends(get_db)):
    try:
        # Consultamos el género por su ID. Si no existe, lanzamos una excepción
        genero = db.query(Genero).filter(Genero.id == genero_id).first()

        # Si el género existe, lo eliminamos. Si no, lanzamos una excepción
        if genero:
            db.delete(genero)
            db.commit()

            user_logger.info(f'Género eliminado: {genero.id}')
            
            return genero
        else:
            raise HTTPException(status_code=404, detail='Género no encontrado')
    except SQLAlchemyError as e:
        internal_logger.error(f'Error al eliminar el género: {str(e)}')
        raise HTTPException(status_code=500, detail='Error eliminando el género')