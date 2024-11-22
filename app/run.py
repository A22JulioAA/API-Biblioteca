# run.py: punto de entrada de la API

# Importamos las librerías necesarias de Python
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import time

# Importamos las librerías/funciones propias
from utilities import get_ip
from database import init_db, get_db, get_db_info

# Modelos para crear las tablas de la base de datos
from models import libro, user, prestamo, prestamo_libros

# Configuramos el logger
logging.basicConfig(
    filename='../api.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )

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

# Logger para la API
logger = logging.getLogger(__name__)

# Inicializamos la base de datos
@app.on_event("startup")
def startup ():
    logger.info('Iniciando la base de datos...')

    try:
        init_db()
        logger.info('Base de datos iniciada correctamente')
    except Exception as e:
        logger.error(f'Error al iniciar la base de datos: {e}')
        raise HTTPException(status_code=500, detail='Error al iniciar la base de datos')

# Endpoint para comprobar que la API está funcionando
@app.get(
        '/check',
        summary='Comprobar que la API está funcionando',
        description='Comprueba que la API está funcionando correctamente',
)
def check():
    ip = get_ip()
    logger.info(f'Peticion a /check: {ip}')
    return {'IP': ip, 'status': 'API en funcionamiento' if ip else 'API no disponible'}

# Endpoint para comprobar la base de datos
@app.get(
        '/db',
        summary='Comprobar la base de datos',
        description='Comprueba que la base de datos está funcionando correctamente',
)
def db():
    logger.info('Peticion a /db. Comprobando base de datos...')

    db_info = get_db_info()

    logger.info(f'Información de la base de datos: {db_info}')

    return db_info

if __name__ == '__main__':
    uvicorn.run(app='run:app', host='0.0.0.0', port=8995, reload=True, reload_excludes=['api.log'])