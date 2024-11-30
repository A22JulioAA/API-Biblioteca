# Rutas para la entidad Libro

# Importamos las librerías necesarias
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Importamos el logger
from log_config import setup_logger

# Importamos las funciones de validación
from validaciones import validar_isbn

# Importamos los modelos y esquemas necesarios
from models.libro import Libro
from schemas.libro_schemas import LibroResponse, LibroCreate

# Importamos la función para obtener la base de datos
from database import get_db

# Creamos el router para los libros
libros_router = APIRouter(
    prefix='/libros',
    tags=['Libros']
)

# Configuramos el logger
user_logger, internal_logger = setup_logger()

# Ruta para obtener todos los libros
@libros_router.get(
    '/',
    description='Obtener todos los libros',
    responses={
        200: {
            'description': 'Lista de libros',
            'model': list[LibroResponse]
        },
        404: {
            'description': 'No hay libros registrados'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def get_libros(db: Session = Depends(get_db)):
    try: 
        # Consultamos los libros de la base de datos. Si no hay libros, se lanza una excepción
        libros = db.query(Libro).all()

        # Si hay libros, los devolvemos. Si no, lanzamos una excepción
        if libros:
            return libros
        else:
            raise HTTPException(status_code=404, detail='No hay libros registrados')
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Ruta para obtener un libro por su ID
@libros_router.get(
    '/{id}',
    description='Obtener un libro por su ID',
    responses={
        200: {
            'description': 'Libro encontrado',
            'model': LibroResponse
        },
        404: {
            'description': 'Libro no encontrado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def get_libro_by_id(id: int, db: Session = Depends(get_db)):
    try:
        # Consultamos el libro por su ID
        libro = db.query(Libro).filter(Libro.id == id).first()

        # Si el libro existe, lo devolvemos. Si no, lanzamos una excepción
        if libro:
            return libro
        else:
            raise HTTPException(status_code=404, detail='Libro no encontrado')

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Ruta para obtener un libro por su ISBN
@libros_router.get(
    '/isbn/{isbn}',
    description='Obtener un libro por su ISBN',
    responses={
        200: {
            'description': 'Libro encontrado',
            'model': LibroResponse
        },
        404: {
            'description': 'Libro no encontrado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def get_libro_by_isbn(isbn: str, db: Session = Depends(get_db)):
    try:
        # Comprobamos que el ISBN tenga 13 caracteres TODO: Podría hacerse una validación de ISBN de 10 dígitos
        validar_isbn(isbn)
        
        # Consultamos el libro por su ISBN
        libro = db.query(Libro).filter(Libro.isbn == isbn).first()

        # Si el libro existe, lo devolvemos. Si no, lanzamos una excepción
        if libro:
            return libro
        else:
            raise HTTPException(status_code=404, detail='Libro no encontrado')

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Ruta para obtener todos los libros de un autor
@libros_router.get(
    '/autor/{autor}',
    description='Obtener todos los libros de un autor',
    responses={
        200: {
            'description': 'Lista de libros',
            'model': LibroResponse
        },
        404: {
            'description': 'No hay libros del autor'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def get_libros_by_autor(autor: str, db: Session = Depends(get_db)):
    try:
        # Consultamos los libros por el autor
        libros = db.query(Libro).filter(Libro.autor == autor).all()

        # Si hay libros, los devolvemos. Si no, lanzamos una excepción
        if libros:
            return libros
        else:
            raise HTTPException(status_code=404, detail='No hay libros del autor')

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Ruta para añadir un libro
@libros_router.post(
    '/',
    description='Añadir un libro',
    responses={
        201: {
            'description': 'Libro añadido',
            'model': LibroResponse
        },
        400: {
            'description': 'Datos incorrectos'
        },
        409: {
            'description': 'El libro ya existe'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def add_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    try:
        # Comprobamos que no haya un libro con el mismo ISBN
        if db.query(Libro).filter(Libro.isbn == libro.isbn).first():
            raise HTTPException(status_code=409, detail=f'El libro con el ISBN - {libro.isbn} - ya existe')

        # Creamos el objeto Libro
        nuevoLibro = Libro(**libro.dict())
        
        # Añadimos la fecha de creación y actualización
        nuevoLibro.created_at = datetime.now()
        nuevoLibro.updated_at = datetime.now()

        # Añadimos el libro a la base de datos
        db.add(nuevoLibro)
        db.commit()
        db.refresh(nuevoLibro)

        user_logger.info(f'Libro añadido: {nuevoLibro.titulo} - {nuevoLibro.isbn}')
        return nuevoLibro

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    