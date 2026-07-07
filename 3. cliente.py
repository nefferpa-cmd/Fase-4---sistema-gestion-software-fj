"""
Módulo para la gestión de clientes.
"""

import re
from excepciones import ClienteDatosInvalidosException, ClienteYaExisteException
from logger_config import logger

class Cliente:
    """
    Clase que representa un cliente del sistema.
    
    Atributos:
        id_cliente (str): Identificador único del cliente
        nombre (str): Nombre completo del cliente
        email (str): Correo electrónico del cliente
        telefono (str): Número de teléfono del cliente
        activo (bool): Estado del cliente
    """
    
    # Variable de clase para asignar IDs automáticos
    _contador_ids = 0
    
    def __init__(self, nombre: str, email: str, telefono: str, id_cliente: str = None):
        """
        Inicializa un nuevo cliente.
        
        Args:
            nombre (str): Nombre completo del cliente
            email (str): Correo electrónico
            telefono (str): Número de teléfono
            id_cliente (str, optional): ID del cliente. Si no se proporciona, se genera automáticamente.
        """
        self._id_cliente = self._generar_id() if id_cliente is None else id_cliente
        self._nombre = self._validar_nombre(nombre)
        self._email = self._validar_email(email)
        self._telefono = self._validar_telefono(telefono)
        self._activo = True
        
        logger.info(f"Cliente creado: {self._nombre} (ID: {self._id_cliente})")
    
    @classmethod
    def _generar_id(cls) -> str:
        """Genera un ID único para el cliente."""
        cls._contador_ids += 1
        return f"CLI-{cls._contador_ids:04d}"
    
    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        """
        Valida el nombre del cliente.
        
        Args:
            nombre (str): Nombre a validar
            
        Returns:
            str: Nombre validado
            
        Raises:
            ClienteDatosInvalidosException: Si el nombre es inválido
        """
        if not nombre or not isinstance(nombre, str):
            logger.error(f"Nombre inválido: {nombre}")
            raise ClienteDatosInvalidosException("El nombre no puede estar vacío")
        
        nombre_limpio = nombre.strip()
        if len(nombre_limpio) < 3:
            logger.error(f"Nombre demasiado corto: {nombre_limpio}")
            raise ClienteDatosInvalidosException("El nombre debe tener al menos 3 caracteres")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_limpio):
            logger.error(f"Nombre con caracteres inválidos: {nombre_limpio}")
            raise ClienteDatosInvalidosException("El nombre solo puede contener letras y espacios")
        
        return nombre_limpio
    
    @staticmethod
    def _validar_email(email: str) -> str:
        """
        Valida el email del cliente.
        
        Args:
            email (str): Email a validar
            
        Returns:
            str: Email validado
            
        Raises:
            ClienteDatosInvalidosException: Si el email es inválido
        """
        if not email:
            logger.error("Email vacío")
            raise ClienteDatosInvalidosException("El email no puede estar vacío")
        
        email_limpio = email.strip().lower()
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(patron, email_limpio):
            logger.error(f"Email inválido: {email_limpio}")
            raise ClienteDatosInvalidosException(f"El email {email_limpio} no es válido")
        
        return email_limpio
    
    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        """
        Valida el teléfono del cliente.
        
        Args:
            telefono (str): Teléfono a validar
            
        Returns:
            str: Teléfono validado
            
        Raises:
            ClienteDatosInvalidosException: Si el teléfono es inválido
        """
        if not telefono:
            logger.error("Teléfono vacío")
            raise ClienteDatosInvalidosException("El teléfono no puede estar vacío")
        
        telefono_limpio = telefono.strip()
        if not re.match(r'^[0-9+\-\s()]{7,20}$', telefono_limpio):
            logger.error(f"Teléfono inválido: {telefono_limpio}")
            raise ClienteDatosInvalidosException(f"El teléfono {telefono_limpio} no es válido")
        
        return telefono_limpio
    
    # Getters y Setters con validaciones
    @property
    def id_cliente(self) -> str:
        return self._id_cliente
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        try:
            self._nombre = self._validar_nombre(nuevo_nombre)
            logger.info(f"Nombre actualizado para cliente {self._id_cliente}: {nuevo_nombre}")
        except ClienteDatosInvalidosException as e:
            logger.error(f"Error al actualizar nombre: {e}")
            raise
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, nuevo_email: str):
        try:
            self._email = self._validar_email(nuevo_email)
            logger.info(f"Email actualizado para cliente {self._id_cliente}: {nuevo_email}")
        except ClienteDatosInvalidosException as e:
            logger.error(f"Error al actualizar email: {e}")
            raise
    
    @property
    def telefono(self) -> str:
        return self._telefono
    
    @telefono.setter
    def telefono(self, nuevo_telefono: str):
        try:
            self._telefono = self._validar_telefono(nuevo_telefono)
            logger.info(f"Teléfono actualizado para cliente {self._id_cliente}: {nuevo_telefono}")
        except ClienteDatosInvalidosException as e:
            logger.error(f"Error al actualizar teléfono: {e}")
            raise
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    def desactivar(self):
        """Desactiva al cliente."""
        self._activo = False
        logger.info(f"Cliente {self._id_cliente} desactivado")
    
    def activar(self):
        """Activa al cliente."""
        self._activo = True
        logger.info(f"Cliente {self._id_cliente} activado")
    
    def __str__(self) -> str:
        return f"Cliente[{self._id_cliente}]: {self._nombre} - {self._email} ({'Activo' if self._activo else 'Inactivo'})"
    
    def __repr__(self) -> str:
        return self.__str__()