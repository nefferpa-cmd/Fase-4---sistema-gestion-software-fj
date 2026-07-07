"""
Módulo para la gestión de servicios.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import ServicioDatosInvalidosException, ServicioNoDisponibleException
from logger_config import logger

class Servicio(ABC):
    """
    Clase abstracta que representa un servicio.
    
    Atributos:
        id_servicio (str): Identificador único del servicio
        nombre (str): Nombre del servicio
        descripcion (str): Descripción del servicio
        precio_base (float): Precio base del servicio
        disponible (bool): Disponibilidad del servicio
    """
    
    _contador_ids = 0
    
    def __init__(self, nombre: str, descripcion: str, precio_base: float):
        """
        Inicializa un nuevo servicio.
        
        Args:
            nombre (str): Nombre del servicio
            descripcion (str): Descripción del servicio
            precio_base (float): Precio base del servicio
        """
        self._id_servicio = self._generar_id()
        self._nombre = self._validar_nombre(nombre)
        self._descripcion = self._validar_descripcion(descripcion)
        self._precio_base = self._validar_precio(precio_base)
        self._disponible = True
        
        logger.info(f"Servicio creado: {self._nombre} (ID: {self._id_servicio})")
    
    @classmethod
    def _generar_id(cls) -> str:
        """Genera un ID único para el servicio."""
        cls._contador_ids += 1
        return f"SERV-{cls._contador_ids:04d}"
    
    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        """Valida el nombre del servicio."""
        if not nombre or not isinstance(nombre, str):
            raise ServicioDatosInvalidosException("El nombre no puede estar vacío")
        nombre_limpio = nombre.strip()
        if len(nombre_limpio) < 3:
            raise ServicioDatosInvalidosException("El nombre debe tener al menos 3 caracteres")
        return nombre_limpio
    
    @staticmethod
    def _validar_descripcion(descripcion: str) -> str:
        """Valida la descripción del servicio."""
        if not descripcion:
            return "Sin descripción"
        return descripcion.strip()
    
    @staticmethod
    def _validar_precio(precio: float) -> float:
        """Valida el precio del servicio."""
        try:
            precio = float(precio)
            if precio < 0:
                raise ServicioDatosInvalidosException("El precio no puede ser negativo")
            return round(precio, 2)
        except (ValueError, TypeError):
            raise ServicioDatosInvalidosException("El precio debe ser un número válido")
    
    @abstractmethod
    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """
        Calcula el costo del servicio.
        
        Args:
            duracion (float): Duración del servicio en horas
            **kwargs: Parámetros adicionales específicos del servicio
            
        Returns:
            float: Costo total del servicio
        """
        pass
    
    @abstractmethod
    def describir_servicio(self) -> str:
        """
        Retorna una descripción detallada del servicio.
        
        Returns:
            str: Descripción del servicio
        """
        pass
    
    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        """
        Valida los parámetros específicos del servicio.
        
        Returns:
            bool: True si los parámetros son válidos
        """
        pass
    
    # Propiedades
    @property
    def id_servicio(self) -> str:
        return self._id_servicio
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def precio_base(self) -> float:
        return self._precio_base
    
    @property
    def disponible(self) -> bool:
        return self._disponible
    
    def cambiar_disponibilidad(self, disponible: bool):
        """Cambia la disponibilidad del servicio."""
        self._disponible = disponible
        estado = "disponible" if disponible else "no disponible"
        logger.info(f"Servicio {self._id_servicio} ahora está {estado}")
    
    def __str__(self) -> str:
        return f"{self._nombre} (ID: {self._id_servicio}) - ${self._precio_base:.2f} {'✓' if self._disponible else '✗'}"

class ReservaSala(Servicio):
    """
    Servicio de reserva de salas.
    """
    
    def __init__(self, nombre: str, descripcion: str, precio_base: float, 
                 capacidad_maxima: int, equipamiento: list = None):
        """
        Inicializa un servicio de reserva de sala.
        
        Args:
            capacidad_maxima (int): Capacidad máxima de la sala
            equipamiento (list): Lista de equipamiento disponible
        """
        super().__init__(nombre, descripcion, precio_base)
        self._capacidad_maxima = self._validar_capacidad(capacidad_maxima)
        self._equipamiento = equipamiento or []
        logger.info(f"Sala creada con capacidad para {self._capacidad_maxima} personas")
    
    @staticmethod
    def _validar_capacidad(capacidad: int) -> int:
        """Valida la capacidad de la sala."""
        try:
            capacidad = int(capacidad)
            if capacidad <= 0:
                raise ServicioDatosInvalidosException("La capacidad debe ser mayor a 0")
            return capacidad
        except (ValueError, TypeError):
            raise ServicioDatosInvalidosException("La capacidad debe ser un número entero")
    
    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """
        Calcula el costo de la reserva de sala.
        
        Args:
            duracion (float): Duración en horas
            **kwargs: 
                - num_personas (int): Número de personas
                - requiere_equipamiento (list): Equipamiento adicional
            
        Returns:
            float: Costo total
        """
        try:
            if duracion <= 0:
                raise ServicioDatosInvalidosException("La duración debe ser mayor a 0")
            
            # Costo base por hora
            costo = self._precio_base * duracion
            
            # Costo adicional por persona si se especifica
            num_personas = kwargs.get('num_personas', 0)
            if num_personas > 0:
                if num_personas > self._capacidad_maxima:
                    raise ServicioDatosInvalidosException(
                        f"La capacidad máxima es {self._capacidad_maxima} personas"
                    )
                # Costo adicional por persona
                costo += num_personas * 2.5
            
            # Costo adicional por equipamiento
            equipamiento_extra = kwargs.get('requiere_equipamiento', [])
            if equipamiento_extra:
                costo += len(equipamiento_extra) * 5.0
            
            # Aplicar descuento si está disponible
            aplicar_descuento = kwargs.get('descuento', False)
            if aplicar_descuento:
                costo = self.aplicar_descuento(costo, kwargs.get('porcentaje_descuento', 10))
            
            return round(costo, 2)
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error en cálculo de costo de sala: {e}")
            raise ServicioDatosInvalidosException(f"Error en cálculo: {e}")
    
    def aplicar_descuento(self, costo: float, porcentaje: float) -> float:
        """Aplica un descuento al costo."""
        try:
            if not (0 <= porcentaje <= 100):
                raise ServicioDatosInvalidosException("El descuento debe estar entre 0 y 100%")
            descuento = costo * (porcentaje / 100)
            return round(costo - descuento, 2)
        except (ValueError, TypeError) as e:
            logger.error(f"Error al aplicar descuento: {e}")
            raise
    
    def describir_servicio(self) -> str:
        return f"Reserva de Sala: {self._nombre}. Capacidad: {self._capacidad_maxima} personas. Equipamiento: {', '.join(self._equipamiento) if self._equipamiento else 'Básico'}"
    
    def validar_parametros(self, **kwargs) -> bool:
        """Valida los parámetros para la reserva de sala."""
        try:
            num_personas = kwargs.get('num_personas', 0)
            if not isinstance(num_personas, int) or num_personas <= 0:
                return False
            
            if num_personas > self._capacidad_maxima:
                return False
            
            duracion = kwargs.get('duracion', 0)
            if not isinstance(duracion, (int, float)) or duracion <= 0:
                return False
            
            return True
        except Exception:
            return False
    
    @property
    def capacidad_maxima(self) -> int:
        return self._capacidad_maxima
    
    @property
    def equipamiento(self) -> list:
        return self._equipamiento.copy()

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos.
    """
    
    def __init__(self, nombre: str, descripcion: str, precio_base: float,
                 equipo: str, especificaciones: dict = None):
        """
        Inicializa un servicio de alquiler de equipo.
        
        Args:
            equipo (str): Nombre del equipo
            especificaciones (dict): Especificaciones del equipo
        """
        super().__init__(nombre, descripcion, precio_base)
        self._equipo = self._validar_equipo(equipo)
        self._especificaciones = especificaciones or {}
        logger.info(f"Equipo creado: {self._equipo}")
    
    @staticmethod
    def _validar_equipo(equipo: str) -> str:
        """Valida el nombre del equipo."""
        if not equipo or not isinstance(equipo, str):
            raise ServicioDatosInvalidosException("El nombre del equipo no puede estar vacío")
        return equipo.strip()
    
    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """
        Calcula el costo del alquiler del equipo.
        
        Args:
            duracion (float): Duración en horas
            **kwargs:
                - incluye_seguro (bool): Si incluye seguro
                - descuento (float): Porcentaje de descuento
        """
        try:
            if duracion <= 0:
                raise ServicioDatosInvalidosException("La duración debe ser mayor a 0")
            
            costo = self._precio_base * duracion
            
            # Costo adicional por seguro
            incluye_seguro = kwargs.get('incluye_seguro', False)
            if incluye_seguro:
                costo += duracion * 3.0
            
            # Descuento por alquiler largo
            if duracion > 24:
                costo = costo * 0.85  # 15% de descuento
            
            # Descuento adicional
            descuento = kwargs.get('descuento', 0)
            if descuento > 0:
                costo = self.aplicar_descuento(costo, descuento)
            
            return round(costo, 2)
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error en cálculo de costo de equipo: {e}")
            raise
    
    def aplicar_descuento(self, costo: float, porcentaje: float) -> float:
        """Aplica un descuento al costo."""
        try:
            if not (0 <= porcentaje <= 100):
                raise ServicioDatosInvalidosException("El descuento debe estar entre 0 y 100%")
            descuento = costo * (porcentaje / 100)
            return round(costo - descuento, 2)
        except (ValueError, TypeError) as e:
            logger.error(f"Error al aplicar descuento: {e}")
            raise
    
    def describir_servicio(self) -> str:
        specs = ", ".join([f"{k}: {v}" for k, v in self._especificaciones.items()])
        return f"Alquiler de {self._equipo}: {self._nombre}. {specs if specs else 'Sin especificaciones adicionales'}"
    
    def validar_parametros(self, **kwargs) -> bool:
        """Valida los parámetros para el alquiler de equipo."""
        try:
            duracion = kwargs.get('duracion', 0)
            if not isinstance(duracion, (int, float)) or duracion <= 0:
                return False
            
            # Verificar que el seguro sea booleano
            if 'incluye_seguro' in kwargs:
                if not isinstance(kwargs['incluye_seguro'], bool):
                    return False
            
            return True
        except Exception:
            return False
    
    @property
    def equipo(self) -> str:
        return self._equipo
    
    @property
    def especificaciones(self) -> dict:
        return self._especificaciones.copy()

class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría especializada.
    """
    
    def __init__(self, nombre: str, descripcion: str, precio_base: float,
                 tema: str, nivel: str = "Básico", duracion_minima: int = 1):
        """
        Inicializa un servicio de asesoría.
        
        Args:
            tema (str): Tema de la asesoría
            nivel (str): Nivel de la asesoría (Básico, Intermedio, Avanzado)
            duracion_minima (int): Duración mínima en horas
        """
        super().__init__(nombre, descripcion, precio_base)
        self._tema = self._validar_tema(tema)
        self._nivel = self._validar_nivel(nivel)
        self._duracion_minima = self._validar_duracion_minima(duracion_minima)
        logger.info(f"Asesoría creada: {self._tema} (Nivel: {self._nivel})")
    
    @staticmethod
    def _validar_tema(tema: str) -> str:
        """Valida el tema de la asesoría."""
        if not tema or not isinstance(tema, str):
            raise ServicioDatosInvalidosException("El tema no puede estar vacío")
        return tema.strip()
    
    @staticmethod
    def _validar_nivel(nivel: str) -> str:
        """Valida el nivel de la asesoría."""
        niveles_validos = ["Básico", "Intermedio", "Avanzado"]
        nivel_limpio = nivel.strip().capitalize()
        if nivel_limpio not in niveles_validos:
            raise ServicioDatosInvalidosException(
                f"Nivel inválido. Debe ser: {', '.join(niveles_validos)}"
            )
        return nivel_limpio
    
    @staticmethod
    def _validar_duracion_minima(duracion: int) -> int:
        """Valida la duración mínima."""
        try:
            duracion = int(duracion)
            if duracion <= 0:
                raise ServicioDatosInvalidosException("La duración mínima debe ser mayor a 0")
            return duracion
        except (ValueError, TypeError):
            raise ServicioDatosInvalidosException("La duración mínima debe ser un número entero")
    
    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """
        Calcula el costo de la asesoría.
        
        Args:
            duracion (float): Duración en horas
            **kwargs:
                - material_incluido (bool): Si incluye material
                - certificado (bool): Si incluye certificado
        """
        try:
            if duracion < self._duracion_minima:
                raise ServicioDatosInvalidosException(
                    f"La duración mínima es de {self._duracion_minima} hora(s)"
                )
            
            # Costo base
            costo = self._precio_base * duracion
            
            # Multiplicador por nivel
            multiplicadores = {"Básico": 1.0, "Intermedio": 1.3, "Avanzado": 1.7}
            costo *= multiplicadores.get(self._nivel, 1.0)
            
            # Costo adicional por material
            if kwargs.get('material_incluido', False):
                costo += duracion * 2.0
            
            # Costo adicional por certificado
            if kwargs.get('certificado', False):
                costo += 15.0
            
            return round(costo, 2)
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error en cálculo de costo de asesoría: {e}")
            raise
    
    def describir_servicio(self) -> str:
        return f"Asesoría de {self._tema} (Nivel {self._nivel}). Duración mínima: {self._duracion_minima}h. {self._descripcion}"
    
    def validar_parametros(self, **kwargs) -> bool:
        """Valida los parámetros para la asesoría."""
        try:
            duracion = kwargs.get('duracion', 0)
            if not isinstance(duracion, (int, float)) or duracion < self._duracion_minima:
                return False
            return True
        except Exception:
            return False
    
    @property
    def tema(self) -> str:
        return self._tema
    
    @property
    def nivel(self) -> str:
        return self._nivel
    
    @property
    def duracion_minima(self) -> int:
        return self._duracion_minima