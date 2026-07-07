"""
Módulo para la gestión de reservas.
"""

from datetime import datetime
from enum import Enum
from excepciones import (
    ReservaInvalidaException, 
    EstadoReservaInvalidoException,
    ServicioNoDisponibleException
)
from logger_config import logger

class EstadoReserva(Enum):
    """Enumeración para los estados de una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"
    FALLIDA = "Fallida"

class Reserva:
    """
    Clase que representa una reserva en el sistema.
    
    Atributos:
        id_reserva (str): Identificador único de la reserva
        cliente: Objeto Cliente asociado
        servicio: Objeto Servicio asociado
        duracion (float): Duración en horas
        fecha_reserva (datetime): Fecha de creación
        estado (EstadoReserva): Estado actual de la reserva
        parametros_extra (dict): Parámetros adicionales
    """
    
    _contador_ids = 0
    
    def __init__(self, cliente, servicio, duracion: float, **kwargs):
        """
        Inicializa una nueva reserva.
        
        Args:
            cliente: Objeto Cliente
            servicio: Objeto Servicio
            duracion (float): Duración en horas
            **kwargs: Parámetros adicionales del servicio
        """
        self._id_reserva = self._generar_id()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = self._validar_duracion(duracion)
        self._fecha_reserva = datetime.now()
        self._estado = EstadoReserva.PENDIENTE
        self._parametros_extra = kwargs
        self._costo_total = None
        
        logger.info(f"Reserva {self._id_reserva} creada para cliente {cliente.nombre}")
    
    @classmethod
    def _generar_id(cls) -> str:
        """Genera un ID único para la reserva."""
        cls._contador_ids += 1
        return f"RES-{cls._contador_ids:04d}"
    
    @staticmethod
    def _validar_duracion(duracion: float) -> float:
        """Valida la duración de la reserva."""
        try:
            duracion = float(duracion)
            if duracion <= 0:
                raise ReservaInvalidaException("La duración debe ser mayor a 0")
            return duracion
        except (ValueError, TypeError):
            raise ReservaInvalidaException("La duración debe ser un número válido")
    
    def confirmar(self) -> bool:
        """
        Confirma la reserva.
        
        Returns:
            bool: True si se confirma exitosamente
            
        Raises:
            ServicioNoDisponibleException: Si el servicio no está disponible
        """
        try:
            if not self._servicio.disponible:
                logger.error(f"Servicio {self._servicio.id_servicio} no disponible")
                raise ServicioNoDisponibleException("El servicio no está disponible")
            
            if self._estado == EstadoReserva.CANCELADA:
                logger.error(f"Reserva {self._id_reserva} ya fue cancelada")
                raise ReservaInvalidaException("No se puede confirmar una reserva cancelada")
            
            if self._estado == EstadoReserva.CONFIRMADA:
                logger.warning(f"Reserva {self._id_reserva} ya está confirmada")
                return True
            
            # Calcular costo total
            self._costo_total = self._servicio.calcular_costo(
                self._duracion, **self._parametros_extra
            )
            
            self._estado = EstadoReserva.CONFIRMADA
            logger.info(f"Reserva {self._id_reserva} confirmada. Costo: ${self._costo_total:.2f}")
            return True
            
        except Exception as e:
            logger.error(f"Error al confirmar reserva {self._id_reserva}: {e}")
            self._estado = EstadoReserva.FALLIDA
            raise
    
    def cancelar(self, motivo: str = "No especificado") -> bool:
        """
        Cancela la reserva.
        
        Returns:
            bool: True si se cancela exitosamente
        """
        try:
            if self._estado in [EstadoReserva.COMPLETADA, EstadoReserva.CANCELADA]:
                logger.warning(f"Reserva {self._id_reserva} ya está {self._estado.value}")
                return False
            
            self._estado = EstadoReserva.CANCELADA
            logger.info(f"Reserva {self._id_reserva} cancelada. Motivo: {motivo}")
            return True
            
        except Exception as e:
            logger.error(f"Error al cancelar reserva {self._id_reserva}: {e}")
            self._estado = EstadoReserva.FALLIDA
            raise
    
    def completar(self) -> bool:
        """
        Marca la reserva como completada.
        
        Returns:
            bool: True si se completa exitosamente
        """
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise ReservaInvalidaException(
                    f"No se puede completar una reserva en estado {self._estado.value}"
                )
            
            self._estado = EstadoReserva.COMPLETADA
            logger.info(f"Reserva {self._id_reserva} completada")
            return True
            
        except Exception as e:
            logger.error(f"Error al completar reserva {self._id_reserva}: {e}")
            raise
    
    def procesar(self) -> dict:
        """
        Procesa la reserva completa, confirmando y calculando todo.
        
        Returns:
            dict: Detalles de la reserva procesada
        """
        try:
            # Intentar confirmar
            self.confirmar()
            
            # Si se confirmó, retornar detalles
            return self.obtener_detalles()
            
        except Exception as e:
            logger.error(f"Error al procesar reserva {self._id_reserva}: {e}")
            self._estado = EstadoReserva.FALLIDA
            raise
    
    def obtener_detalles(self) -> dict:
        """
        Obtiene los detalles completos de la reserva.
        
        Returns:
            dict: Diccionario con todos los detalles
        """
        return {
            'id_reserva': self._id_reserva,
            'cliente': {
                'id': self._cliente.id_cliente,
                'nombre': self._cliente.nombre,
                'email': self._cliente.email
            },
            'servicio': {
                'id': self._servicio.id_servicio,
                'nombre': self._servicio.nombre,
                'tipo': self._servicio.__class__.__name__
            },
            'duracion': self._duracion,
            'fecha': self._fecha_reserva.strftime('%Y-%m-%d %H:%M:%S'),
            'estado': self._estado.value,
            'costo_total': self._costo_total,
            'parametros': self._parametros_extra
        }
    
    # Propiedades
    @property
    def id_reserva(self) -> str:
        return self._id_reserva
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def servicio(self):
        return self._servicio
    
    @property
    def duracion(self) -> float:
        return self._duracion
    
    @property
    def fecha_reserva(self) -> datetime:
        return self._fecha_reserva
    
    @property
    def estado(self) -> EstadoReserva:
        return self._estado
    
    @property
    def costo_total(self) -> float:
        return self._costo_total
    
    def __str__(self) -> str:
        return f"Reserva {self._id_reserva}: {self._cliente.nombre} - {self._servicio.nombre} ({self._estado.value})"