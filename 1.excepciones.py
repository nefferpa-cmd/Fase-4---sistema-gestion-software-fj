"""
Módulo para la gestión de excepciones personalizadas del sistema.
"""

class SistemaException(Exception):
    """Excepción base para el sistema."""
    pass

class ClienteException(SistemaException):
    """Excepción relacionada con operaciones de clientes."""
    pass

class ClienteNoEncontradoException(ClienteException):
    """Excepción cuando un cliente no existe."""
    pass

class ClienteYaExisteException(ClienteException):
    """Excepción cuando un cliente ya existe."""
    pass

class ClienteDatosInvalidosException(ClienteException):
    """Excepción cuando los datos del cliente son inválidos."""
    pass

class ServicioException(SistemaException):
    """Excepción relacionada con operaciones de servicios."""
    pass

class ServicioNoDisponibleException(ServicioException):
    """Excepción cuando un servicio no está disponible."""
    pass

class ServicioNoEncontradoException(ServicioException):
    """Excepción cuando un servicio no existe."""
    pass

class ServicioDatosInvalidosException(ServicioException):
    """Excepción cuando los datos del servicio son inválidos."""
    pass

class ReservaException(SistemaException):
    """Excepción relacionada con operaciones de reservas."""
    pass

class ReservaInvalidaException(ReservaException):
    """Excepción cuando una reserva es inválida."""
    pass

class ReservaYaExisteException(ReservaException):
    """Excepción cuando una reserva ya existe."""
    pass

class ReservaNoEncontradaException(ReservaException):
    """Excepción cuando una reserva no existe."""
    pass

class EstadoReservaInvalidoException(ReservaException):
    """Excepción cuando el estado de la reserva es inválido."""
    pass

class CalculoException(SistemaException):
    """Excepción relacionada con cálculos."""
    pass