# Rutas para la entidad Libro

# Importamos las librerías necesarias
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Importamos el logger
from log_config import setup_logger

# Importamos las funciones de validación
from validaciones import validar_isbn

# Importamos las funciones necesarias para crear el pdf
from functions import generar_pdf

# Importamos los modelos y esquemas necesarios
from models.libro import Libro
from schemas.libro_schemas import LibroResponse, LibroCreate
from models.genero import Genero

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
    response_model=list[LibroResponse],
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
        internal_logger.error(f'Error al obtener los libros: {str(e)}')
        raise HTTPException(status_code=500, detail='Error obteniendo los libros')
    
# Ruta para obtener un libro por su ID
@libros_router.get(
    '/{id}',
    description='Obtener un libro por su ID',
    response_model=LibroResponse,
    responses={
        200: {
            'description': 'Libro encontrado',
            'model': LibroResponse
        },
        404: {
            'description': 'Libro no encontrado'
        },
        422: {
            'description': 'ID incorrecto'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def get_libro_by_id(id: int = Path(..., ge=1, description='ID del libro'), db: Session = Depends(get_db)):
    try:
        # Consultamos el libro por su ID
        libro = db.query(Libro).filter(Libro.id == id).first()

        # Si el libro existe, lo devolvemos. Si no, lanzamos una excepción
        if libro:
            return libro
        else:
            raise HTTPException(status_code=404, detail='Libro no encontrado')

    except SQLAlchemyError as e:
        internal_logger.error(f'Error al obtener el libro: {str(e)}')
        raise HTTPException(status_code=500, detail='Error obteniendo el libro')
    
# Ruta para obtener un libro por su ISBN
@libros_router.get(
    '/isbn/{isbn}',
    description='Obtener un libro por su ISBN',
    response_model=LibroResponse,
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
async def get_libro_by_isbn(isbn: str = Path(..., min_length=10, description='ISBN del libro (10 caracteres mín.)'), db: Session = Depends(get_db)):
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
        internal_logger.error(f'Error al obtener el libro: {str(e)}')
        raise HTTPException(status_code=500, detail='Error obteniendo el libro')
    
# Ruta para obtener todos los libros de un autor
@libros_router.get(
    '/autor/{autor}',
    description='Obtener todos los libros de un autor',
    response_model=list[LibroResponse],
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
async def get_libros_by_autor(autor: str = Path(..., description = 'Nombre del autor'), db: Session = Depends(get_db)):
    try:
        # Consultamos los libros por el autor
        libros = db.query(Libro).filter(Libro.autor == autor).all()

        # Si hay libros, los devolvemos. Si no, lanzamos una excepción
        if libros:
            return libros
        else:
            raise HTTPException(status_code=404, detail='No hay libros del autor')

    except SQLAlchemyError as e:
        internal_logger.error(f'Error al obtener los libros: {str(e)}')
        raise HTTPException(status_code=500, detail='Error obteniendo los libros')
    
# Ruta para añadir un libro
@libros_router.post(
    '/',
    description='Añadir un libro',
    response_model=LibroResponse,
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
        # Comprobamos que el ISBN sea correcto
        validar_isbn(libro.isbn)
        # Comprobamos que no haya un libro con el mismo ISBN
        if db.query(Libro).filter(Libro.isbn == libro.isbn).first():
            raise HTTPException(status_code=409, detail=f'El libro con el ISBN - {libro.isbn} - ya existe')
        
        # Obtenemos los géneros del libro
        if libro.generos:
            generos = db.query(Genero).filter(Genero.id.in_(libro.generos)).all()

            if len(generos) != len(libro.generos):
                raise HTTPException(status_code=400, detail='Uno o más géneros no existen')

        # Creamos el objeto Libro
        nuevoLibro = Libro(
            isbn=libro.isbn,
            titulo=libro.titulo,
            autor=libro.autor,
            descripcion=libro.descripcion,
            editorial=libro.editorial,
            pais=libro.pais,
            idioma=libro.idioma,
            num_paginas=libro.num_paginas,
            ano_edicion=libro.ano_edicion,
            precio=libro.precio,
            generos=generos,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

        # Añadimos el libro a la base de datos
        db.add(nuevoLibro)
        db.commit()
        db.refresh(nuevoLibro)

        user_logger.info(f'Libro añadido: {nuevoLibro.titulo} - {nuevoLibro.isbn}')
        return nuevoLibro

    except SQLAlchemyError as e:
        internal_logger.error(f'Error al añadir el libro: {str(e)}')
        raise HTTPException(status_code=500, detail='Error añadiendo el libro')
    
# Ruta para descargar un PDF con la lista de libros
@libros_router.get(
    '/pdf',
    description='Descargar un PDF con la lista de libros',
    responses={
        200: {
            'description': 'PDF descargado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def download_pdf(db: Session = Depends(get_db)):
    try:
        # Consultamos los libros de la base de datos
        libros = db.query(Libro).all()

        # Si no hay libros, lanzamos una excepción
        if not libros:
            raise HTTPException(status_code=404, detail='No hay libros registrados')
        
        # Generamos el PDF
        generar_pdf(libros, 'lista_libros.pdf')
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
