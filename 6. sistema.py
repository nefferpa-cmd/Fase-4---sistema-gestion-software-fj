"""
Módulo principal del sistema de gestión.
"""

from typing import List, Optional
from excepciones import (
    ClienteNoEncontradoException, ClienteYaExisteException,
    ServicioNoEncontradoException, ReservaNoEncontradaException,
    ReservaInvalidaException
)
from logger_config import logger

class SistemaGestion:
    """
    Clase principal del sistema de gestión.
    """
    
    def __init__(self):
        """Inicializa el sistema."""
        self._clientes = []
        self._servicios = []
        self._reservas = []
        logger.info("Sistema de Gestión inicializado")
    
    # ============ MÉTODOS PARA CLIENTES ============
    
    def registrar_cliente(self, cliente) -> bool:
        """
        Registra un nuevo cliente en el sistema.
        
        Args:
            cliente: Objeto Cliente
            
        Returns:
            bool: True si se registra exitosamente
            
        Raises:
            ClienteYaExisteException: Si el cliente ya existe
        """
        try:
            # Verificar si ya existe
            for c in self._clientes:
                if c.id_cliente == cliente.id_cliente:
                    raise ClienteYaExisteException(
                        f"Cliente con ID {cliente.id_cliente} ya existe"
                    )
            
            self._clientes.append(cliente)
            logger.info(f"Cliente registrado en el sistema: {cliente.nombre}")
            return True
            
        except Exception as e:
            logger.error(f"Error al registrar cliente: {e}")
            raise
    
    def buscar_cliente(self, id_cliente: str):
        """
        Busca un cliente por su ID.
        
        Args:
            id_cliente (str): ID del cliente
            
        Returns:
            Cliente: Objeto Cliente encontrado
            
        Raises:
            ClienteNoEncontradoException: Si el cliente no existe
        """
        for cliente in self._clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        
        raise ClienteNoEncontradoException(f"Cliente con ID {id_cliente} no encontrado")
    
    def listar_clientes(self) -> List:
        """
        Lista todos los clientes del sistema.
        
        Returns:
            List: Lista de clientes
        """
        return self._clientes.copy()
    
    def eliminar_cliente(self, id_cliente: str) -> bool:
        """
        Elimina un cliente del sistema (lo desactiva).
        
        Args:
            id_cliente (str): ID del cliente
            
        Returns:
            bool: True si se elimina exitosamente
        """
        try:
            cliente = self.buscar_cliente(id_cliente)
            cliente.desactivar()
            logger.info(f"Cliente {id_cliente} eliminado del sistema")
            return True
        except ClienteNoEncontradoException:
            logger.warning(f"Intento de eliminar cliente no encontrado: {id_cliente}")
            raise
    
    # ============ MÉTODOS PARA SERVICIOS ============
    
    def registrar_servicio(self, servicio) -> bool:
        """
        Registra un nuevo servicio en el sistema.
        
        Args:
            servicio: Objeto Servicio
            
        Returns:
            bool: True si se registra exitosamente
        """
        try:
            self._servicios.append(servicio)
            logger.info(f"Servicio registrado en el sistema: {servicio.nombre}")
            return True
        except Exception as e:
            logger.error(f"Error al registrar servicio: {e}")
            raise
    
    def buscar_servicio(self, id_servicio: str):
        """
        Busca un servicio por su ID.
        
        Args:
            id_servicio (str): ID del servicio
            
        Returns:
            Servicio: Objeto Servicio encontrado
            
        Raises:
            ServicioNoEncontradoException: Si el servicio no existe
        """
        for servicio in self._servicios:
            if servicio.id_servicio == id_servicio:
                return servicio
        
        raise ServicioNoEncontradoException(f"Servicio con ID {id_servicio} no encontrado")
    
    def listar_servicios(self) -> List:
        """
        Lista todos los servicios del sistema.
        
        Returns:
            List: Lista de servicios
        """
        return self._servicios.copy()
    
    def listar_servicios_disponibles(self) -> List:
        """
        Lista los servicios disponibles.
        
        Returns:
            List: Lista de servicios disponibles
        """
        return [s for s in self._servicios if s.disponible]
    
    # ============ MÉTODOS PARA RESERVAS ============
    
    def crear_reserva(self, id_cliente: str, id_servicio: str, duracion: float, **kwargs):
        """
        Crea una nueva reserva.
        
        Args:
            id_cliente (str): ID del cliente
            id_servicio (str): ID del servicio
            duracion (float): Duración en horas
            **kwargs: Parámetros adicionales
            
        Returns:
            Reserva: Objeto Reserva creado
            
        Raises:
            ClienteNoEncontradoException: Si el cliente no existe
            ServicioNoEncontradoException: Si el servicio no existe
        """
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            
            if not cliente.activo:
                raise ReservaInvalidaException("El cliente no está activo")
            
            # Validar parámetros del servicio
            if not servicio.validar_parametros(duracion=duracion, **kwargs):
                raise ReservaInvalidaException("Parámetros inválidos para el servicio")
            
            reserva = Reserva(cliente, servicio, duracion, **kwargs)
            self._reservas.append(reserva)
            
            logger.info(f"Reserva creada: {reserva.id_reserva}")
            return reserva
            
        except Exception as e:
            logger.error(f"Error al crear reserva: {e}")
            raise
    
    def confirmar_reserva(self, id_reserva: str) -> dict:
        """
        Confirma una reserva existente.
        
        Args:
            id_reserva (str): ID de la reserva
            
        Returns:
            dict: Detalles de la reserva confirmada
        """
        try:
            reserva = self.buscar_reserva(id_reserva)
            return reserva.procesar()
        except Exception as e:
            logger.error(f"Error al confirmar reserva {id_reserva}: {e}")
            raise
    
    def cancelar_reserva(self, id_reserva: str, motivo: str = "Cancelado por el cliente") -> bool:
        """
        Cancela una reserva.
        
        Args:
            id_reserva (str): ID de la reserva
            motivo (str): Motivo de la cancelación
        """
        try:
            reserva = self.buscar_reserva(id_reserva)
            return reserva.cancelar(motivo)
        except Exception as e:
            logger.error(f"Error al cancelar reserva {id_reserva}: {e}")
            raise
    
    def buscar_reserva(self, id_reserva: str):
        """
        Busca una reserva por su ID.
        
        Args:
            id_reserva (str): ID de la reserva
            
        Returns:
            Reserva: Objeto Reserva encontrado
        """
        for reserva in self._reservas:
            if reserva.id_reserva == id_reserva:
                return reserva
        
        raise ReservaNoEncontradaException(f"Reserva con ID {id_reserva} no encontrada")
    
    def listar_reservas(self) -> List:
        """
        Lista todas las reservas del sistema.
        
        Returns:
            List: Lista de reservas
        """
        return self._reservas.copy()
    
    def listar_reservas_por_cliente(self, id_cliente: str) -> List:
        """
        Lista las reservas de un cliente específico.
        
        Args:
            id_cliente (str): ID del cliente
            
        Returns:
            List: Lista de reservas del cliente
        """
        try:
            cliente = self.buscar_cliente(id_cliente)
            return [r for r in self._reservas if r.cliente.id_cliente == cliente.id_cliente]
        except ClienteNoEncontradoException:
            logger.warning(f"Cliente {id_cliente} no encontrado para listar reservas")
            return []
    
    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del sistema.
        
        Returns:
            dict: Estadísticas
        """
        return {
            'total_clientes': len(self._clientes),
            'clientes_activos': len([c for c in self._clientes if c.activo]),
            'total_servicios': len(self._servicios),
            'servicios_disponibles': len([s for s in self._servicios if s.disponible]),
            'total_reservas': len(self._reservas),
            'reservas_confirmadas': len([r for r in self._reservas if r.estado.value == "Confirmada"]),
            'reservas_pendientes': len([r for r in self._reservas if r.estado.value == "Pendiente"]),
            'reservas_canceladas': len([r for r in self._reservas if r.estado.value == "Cancelada"])
        }