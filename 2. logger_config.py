"""
Módulo para la configuración del sistema de logging.
"""

import logging
import os
from datetime import datetime

def configurar_logger():
    """
    Configura el logger para el sistema.
    
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Nombre del archivo de log con fecha
    fecha = datetime.now().strftime('%Y%m%d')
    nombre_archivo = f'logs/sistema_{fecha}.log'
    
    # Configurar logger
    logger = logging.getLogger('SistemaGestion')
    logger.setLevel(logging.DEBUG)
    
    # Eliminar handlers existentes para evitar duplicados
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Handler para archivo
    file_handler = logging.FileHandler(nombre_archivo, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global para usar en todo el sistema
logger = configurar_logger()