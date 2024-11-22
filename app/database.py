# Configuración de la base de datos

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# URL de conexión a la base de datos
# TODO: Sacar datos de archivo .env

# Datos de user
user = 'postgres'
# Datos de password
password = 'abc123.'
# Datos de host
host = 'localhost'
# Datos de puerto
port = '5432' # Puerto por defecto de PostgreSQL / No es necesario ponerlo, falla
# Nombre de la base de datos
dbname = 'biblioteca_db'

DATABASE_URL = f'postgresql://{user}:{password}@{host}/{dbname}'

# Crear motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base para las clases de base de datos
Base = declarative_base()

# Función para inicializar la base de datos
def init_db():
    """
    Función para inicializar la base de datos

    """
    Base.metadata.create_all(bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    """
    Función para obtener la sesión de la base de datos

    Returns:
    SessionLocal: Sesión de la base de datos

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_info ():
    """
    Función para obtener la información de la base de datos

    Returns:
    str: Información de la base de datos

    """
    
    try:
        inspector = inspect(engine)

        tablas = inspector.get_table_names()

        db_info = {
            'status': 'Base de datos en funcionamiento',
            'url': str(engine.url),
            'tablas': tablas,
            'num_tablas': len(tablas),
        }

        return db_info
    except SQLAlchemyError as e:
        return {
            'status': f'Error en la base de datos: {e}',
            'url': str(engine.url),
        }
    
def insertar_datos_ejemplo ():
    """
    Función para insertar datos de ejemplo en la base de datos

    """
    from models.libro import Libro
    from models.user import User
    from models.prestamo import Prestamo

    from datetime import datetime

    db = SessionLocal()

    libro1 = db.query(Libro).filter(Libro.id == 1).first()
    libro2 = db.query(Libro).filter(Libro.id == 2).first()

    prestamo = Prestamo(
        fecha_prestamo=datetime.now(),
        fecha_devolucion=datetime.now(),
        usuario_id=3,
        libros=[libro1, libro2],
    )


    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)