import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    # Crea el directorio de logs si no existe
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Logger para usuarios
    user_logger = logging.getLogger('user_activity')
    user_logger.setLevel(logging.INFO)

    # Logger interno
    internal_logger = logging.getLogger('internal_activity')
    internal_logger.setLevel(logging.DEBUG)

    if not user_logger.handlers:
        # Formato de logs
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        # Handler para logs de usuarios
        file_handler = RotatingFileHandler('logs/user_activity.log', maxBytes=5_000_000, backupCount=3)
        file_handler.setFormatter(formatter)

        # Handler para logs internos
        internal_file_handler = RotatingFileHandler('logs/internal_activity.log', maxBytes=5_000_000, backupCount=3)
        internal_file_handler.setFormatter(formatter)

        # Añadir los handlers a los loggers
        user_logger.addHandler(file_handler)
        internal_logger.addHandler(internal_file_handler)

    return user_logger, internal_logger