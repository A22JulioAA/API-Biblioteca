# run.py: punto de entrada de la API

# Importamos las librerías necesarias de Python
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
import time

# Importamos el logger de la API
from log_config import setup_logger

# Importamos las librerías/funciones propias
from utilities import get_ip
from database import init_db, get_db, get_db_info, insertar_datos_ejemplo

# Modelos para crear las tablas de la base de datos
from models import libro, user, prestamo, prestamo_libros, genero, libros_generos

# Importamos las rutas de la API
from routes.r_libro import libros_router

# Inicializamos el logger
user_logger, internal_logger = setup_logger()

app = FastAPI(
    title='API básica biblioteca',
    description='API básica para biblioteca',
    terms_of_service='http://example.com/terms/',
    version='0.0.1',
    contact={
        'name': 'Xulio',
        'url': 'http://example.com/contact/',
        'email': 'jaa.aller.acuna@gmail.com',
    },
    license_info={
        'name': 'GNU Affero General Public License v3',
        'url': 'https://www.gnu.org/licenses/agpl-3.0.html',
    },
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    user_logger.info(f"{request.client.host} - {request.method} - {request.url.path} - {response.status_code} - {process_time:.2f}ms")

    return response


# Añadimos las rutas a la API
app.include_router(libros_router)

# Inicializamos la base de datos
@app.on_event("startup")
def startup ():
    internal_logger.info('Iniciando la base de datos...')

    try:
        init_db()
        internal_logger.info('Base de datos iniciada correctamente')
    except Exception as e:
        internal_logger.error(f'Error al iniciar la base de datos: {e}')
        raise HTTPException(status_code=500, detail='Error al iniciar la base de datos')

# Endpoint para comprobar que la API está funcionando
@app.get(
        '/check',
        summary='Comprobar que la API está funcionando',
        description='Comprueba que la API está funcionando correctamente',
)
def check():
    ip = get_ip()
    internal_logger.info(f'Peticion a /check: {ip}')
    return {'IP': ip, 'status': 'API en funcionamiento' if ip else 'API no disponible'}

# Endpoint para comprobar la base de datos
@app.get(
        '/db',
        summary='Comprobar la base de datos',
        description='Comprueba que la base de datos está funcionando correctamente',
)
def db():
    internal_logger.info('Peticion a /db. Comprobando base de datos...')

    db_info = get_db_info()

    internal_logger.info(f'Información de la base de datos: {db_info}')

    return db_info

if __name__ == '__main__':
    uvicorn.run(app='run:app', host='0.0.0.0', port=8995, reload=True, reload_excludes=['api.log'])