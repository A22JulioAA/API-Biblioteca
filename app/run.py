# run.py: punto de entrada de la API

# Importamos las librerías necesarias de Python
import logging
import uvicorn
from fastapi import FastAPI
import time

# Importamos las librerías/funciones propias
from utilities import get_ip

# Configuramos el logger
logging.basicConfig(
    filename='api.log',
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

# Endpoint para comprobar que la API está funcionando
@app.get('/check')
def check():
    ip = get_ip()
    logger.info(f'Peticion a /check: {ip}')
    return {'IP': ip, 'status': 'API en funcionamiento' if ip else 'API no disponible'}

if __name__ == '__main__':
    uvicorn.run(app='run:app', host='0.0.0.0', port=8995, reload=True)