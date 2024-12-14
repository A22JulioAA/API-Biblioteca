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
from schemas.libro_schemas import LibroResponse, LibroCreate, LibroUpdate
from models.genero import Genero
from models.autor import Autor

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
        # ----------------------------- VALIDACIONES -----------------------------
        # Comprobamos que el ISBN sea correcto
        validar_isbn(libro.isbn)
        # Comprobamos que no haya un libro con el mismo ISBN
        if db.query(Libro).filter(Libro.isbn == libro.isbn).first():
            raise HTTPException(status_code=409, detail=f'El libro con el ISBN - {libro.isbn} - ya existe')
        
        # ----------------------------- OBTENCIÓN DE DATOS -----------------------------
        # Obtenemos los géneros del libro
        if libro.generos:
            generos = db.query(Genero).filter(Genero.id.in_(libro.generos)).all()

            if len(generos) != len(libro.generos):
                raise HTTPException(status_code=400, detail='Uno o más géneros no existen')

        # Obtenemos los autores del libro
        if libro.autores:
            autores = db.query(Autor).filter(Autor.id.in_(libro.autores)).all()

            if len(autores) != len(libro.autores):
                raise HTTPException(status_code=400, detail='Uno o más autores no existen')
            
        print(autores)
        print(generos)

        # ----------------------------- CREACIÓN DEL OBJETO LIBRO -----------------------------
        # Creamos el objeto Libro
        nuevoLibro = Libro(
            isbn=libro.isbn,
            titulo=libro.titulo,
            autores=autores,
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
        
        return LibroResponse(
            id=nuevoLibro.id,
            isbn=nuevoLibro.isbn,
            titulo=nuevoLibro.titulo,
            autores=[autor.id for autor in nuevoLibro.autores],
            generos=[genero.id for genero in nuevoLibro.generos], 
            descripcion=nuevoLibro.descripcion,
            editorial=nuevoLibro.editorial,
            pais=nuevoLibro.pais,
            idioma=nuevoLibro.idioma,
            num_paginas=nuevoLibro.num_paginas,
            ano_edicion=nuevoLibro.ano_edicion,
            precio=float(nuevoLibro.precio) if nuevoLibro.precio else None,
            created_at=nuevoLibro.created_at,
            updated_at=nuevoLibro.updated_at,
        )

    except SQLAlchemyError as e:
        internal_logger.error(f'Error al añadir el libro: {str(e)}')
        raise HTTPException(status_code=500, detail='Error añadiendo el libro')
    
# Ruta para actualizar un libro
@libros_router.put(
    '/{id}',
    description='Actualizar un libro',
    response_model=LibroResponse,
    responses={
        200: {
            'description': 'Libro actualizado',
            'model': LibroResponse
        },
        400: {
            'description': 'Datos incorrectos'
        },
        404: {
            'description': 'Libro no encontrado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def update_libro(libro_update: LibroUpdate, id: int = Path(..., ge=1, description='ID del libro'), db: Session = Depends(get_db)):
    try:
        libro = db.query(Libro).filter(Libro.id == id).first()

        # Si el libro no existe, lanzamos una excepción
        if not libro:
            raise HTTPException(status_code=404, detail='Libro no encontrado')
        
        # Obtenemos los géneros del libro
        if libro_update.generos:
            generos = db.query(Genero).filter(Genero.id.in_(libro_update.generos)).all()

            if len(generos) != len(libro_update.generos):
                raise HTTPException(status_code=400, detail='Uno o más géneros no existen')
            
        if libro_update.isbn and libro.isbn != libro_update.isbn:
            validar_isbn(libro_update.isbn)
            if db.query(Libro).filter(Libro.isbn == libro_update.isbn).first():
                raise HTTPException(status_code=409, detail=f'El libro con el ISBN - {libro_update.isbn} - ya existe')
            
        # Actualizamos los datos del libro
        if libro_update.isbn:
            libro.isbn = libro_update.isbn
        if libro_update.titulo:
            libro.titulo = libro_update.titulo
        if libro_update.autor:
            libro.autor = libro_update.autor
        if libro_update.descripcion:
            libro.descripcion = libro_update.descripcion
        if libro_update.editorial:
            libro.editorial = libro_update.editorial
        if libro_update.pais:
            libro.pais = libro_update.pais
        if libro_update.idioma:
            libro.idioma = libro_update.idioma
        if libro_update.num_paginas:
            libro.num_paginas = libro_update.num_paginas
        if libro_update.ano_edicion:
            libro.ano_edicion = libro_update.ano_edicion
        if libro_update.precio:
            libro.precio = libro_update.precio
        if libro_update.generos:
            generos = db.query(Genero).filter(Genero.id.in_(libro_update.generos)).all()
            libro.generos = generos

        # Actualizamos la fecha de actualización
        libro.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Guardamos los cambios en la base de datos
        db.commit()
        db.refresh(libro)

        user_logger.info(f'Libro actualizado: {libro.titulo} - {libro.isbn}')
        return libro
    
    except SQLAlchemyError as e:
        internal_logger.error(f'Error al actualizar el libro: {str(e)}')
        raise HTTPException(status_code=500, detail='Error actualizando el libro')

# Ruta para eliminar un libro
@libros_router.delete(
    '/{id}',
    description='Eliminar un libro',
    responses={
        204: {
            'description': 'Libro eliminado'
        },
        404: {
            'description': 'Libro no encontrado'
        },
        500: {
            'description': 'Error del servidor'
        }
    }
)
async def delete_libro(id: int = Path(..., ge=1, description='ID del libro'), db: Session = Depends(get_db)):
    try:
        # Consultamos el libro por su ID
        libro = db.query(Libro).filter(Libro.id == id).first()

        # Si el libro no existe, lanzamos una excepción
        if not libro:
            raise HTTPException(status_code=404, detail='Libro no encontrado')
        
        # Eliminamos el libro
        db.delete(libro)
        db.commit()

        user_logger.info(f'Libro eliminado: {libro.titulo} - {libro.isbn}')
        return None

    except SQLAlchemyError as e:
        internal_logger.error(f'Error al eliminar el libro: {str(e)}')
        raise HTTPException(status_code=500, detail='Error eliminando el libro')


# Ruta para descargar un PDF con la lista de libros
@libros_router.get(
    '/pdf/download',
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
