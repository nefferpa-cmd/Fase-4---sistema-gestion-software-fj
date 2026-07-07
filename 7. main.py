"""
Módulo principal para la simulación del sistema.
"""

import sys
import traceback
from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SistemaGestion
from excepciones import (
    ClienteDatosInvalidosException, ClienteYaExisteException,
    ServicioDatosInvalidosException, ServicioNoDisponibleException,
    ReservaInvalidaException
)
from logger_config import logger

def simular_operaciones():
    """
    Realiza la simulación de operaciones del sistema.
    """
    print("\n" + "="*60)
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("Software FJ")
    print("="*60)
    
    # Inicializar sistema
    sistema = SistemaGestion()
    
    # Lista para almacenar resultados de operaciones
    operaciones = []
    exitosas = 0
    fallidas = 0
    
    # ============================================================
    # 1. REGISTRO DE CLIENTES (VÁLIDOS E INVÁLIDOS)
    # ============================================================
    print("\n--- REGISTRO DE CLIENTES ---")
    
    # Clientes válidos
    clientes_validos = [
        ("Ana María Rodríguez", "ana.rodriguez@email.com", "3001234567"),
        ("Carlos Pérez Gómez", "carlos.perez@email.com", "3209876543"),
        ("María López García", "maria.lopez@email.com", "3104567890"),
        ("Juan Martínez Soto", "juan.martinez@email.com", "3156789012"),
        ("Laura Fernández Díaz", "laura.fernandez@email.com", "3012345678")
    ]
    
    # Registrar clientes válidos
    for nombre, email, telefono in clientes_validos:
        try:
            cliente = Cliente(nombre, email, telefono)
            sistema.registrar_cliente(cliente)
            operaciones.append(f"✅ Cliente registrado: {cliente.nombre} (ID: {cliente.id_cliente})")
            exitosas += 1
            print(f"✅ Cliente registrado: {cliente.nombre} (ID: {cliente.id_cliente})")
        except Exception as e:
            operaciones.append(f"❌ Error al registrar cliente {nombre}: {e}")
            fallidas += 1
            print(f"❌ Error: {e}")
    
    # Clientes inválidos (para probar excepciones)
    print("\n--- Intentando registrar clientes inválidos ---")
    
    casos_invalidos = [
        ("A", "valid@email.com", "3001234567"),  # Nombre muy corto
        ("Nombre Válido", "email-invalido", "3001234567"),  # Email inválido
        ("Nombre Válido", "valid@email.com", "123"),  # Teléfono inválido
        ("Nombre Válido", "valid@email.com", "3001234567"),  # Cliente ya existe (se duplica)
    ]
    
    for nombre, email, telefono in casos_invalidos:
        try:
            cliente = Cliente(nombre, email, telefono)
            sistema.registrar_cliente(cliente)
            operaciones.append(f"✅ Cliente registrado inesperadamente: {cliente.nombre}")
            exitosas += 1
        except Exception as e:
            operaciones.append(f"❌ Error controlado al registrar cliente {nombre}: {e}")
            fallidas += 1
            print(f"❌ Error controlado: {e}")
    
    # ============================================================
    # 2. REGISTRO DE SERVICIOS
    # ============================================================
    print("\n--- REGISTRO DE SERVICIOS ---")
    
    servicios_creados = []
    
    try:
        # Servicio 1: Reserva de Sala
        sala = ReservaSala(
            nombre="Sala Premium",
            descripcion="Sala de conferencias con equipamiento completo",
            precio_base=50.0,
            capacidad_maxima=20,
            equipamiento=["Proyector", "Pizarra digital", "Sistema de audio"]
        )
        sistema.registrar_servicio(sala)
        servicios_creados.append(sala)
        print(f"✅ Servicio creado: {sala.describir_servicio()}")
        exitosas += 1
    except Exception as e:
        print(f"❌ Error al crear servicio: {e}")
        fallidas += 1
    
    try:
        # Servicio 2: Alquiler de Equipo
        equipo = AlquilerEquipo(
            nombre="Laptop Gaming",
            descripcion="Laptop de alto rendimiento para gaming",
            precio_base=30.0,
            equipo="Laptop ASUS ROG",
            especificaciones={"RAM": "16GB", "Almacenamiento": "1TB SSD", "GPU": "RTX 3060"}
        )
        sistema.registrar_servicio(equipo)
        servicios_creados.append(equipo)
        print(f"✅ Servicio creado: {equipo.describir_servicio()}")
        exitosas += 1
    except Exception as e:
        print(f"❌ Error al crear servicio: {e}")
        fallidas += 1
    
    try:
        # Servicio 3: Asesoría Especializada
        asesoria = AsesoriaEspecializada(
            nombre="Asesoría en Python Avanzado",
            descripcion="Curso intensivo de programación en Python",
            precio_base=80.0,
            tema="Programación en Python",
            nivel="Avanzado",
            duracion_minima=2
        )
        sistema.registrar_servicio(asesoria)
        servicios_creados.append(asesoria)
        print(f"✅ Servicio creado: {asesoria.describir_servicio()}")
        exitosas += 1
    except Exception as e:
        print(f"❌ Error al crear servicio: {e}")
        fallidas += 1
    
    # Servicio inválido (para probar excepciones)
    print("\n--- Intentando crear servicio inválido ---")
    try:
        sala_invalida = ReservaSala(
            nombre="Sala Inválida",
            descripcion="Prueba de error",
            precio_base=-10.0,  # Precio negativo
            capacidad_maxima=0  # Capacidad inválida
        )
        sistema.registrar_servicio(sala_invalida)
        print(f"✅ Servicio creado inesperadamente")
    except ServicioDatosInvalidosException as e:
        print(f"❌ Error controlado al crear servicio: {e}")
        fallidas += 1
        operaciones.append(f"❌ Error controlado al crear servicio: {e}")
    
    # ============================================================
    # 3. CREACIÓN DE RESERVAS
    # ============================================================
    print("\n--- CREACIÓN DE RESERVAS ---")
    
    # Obtener IDs para las operaciones
    try:
        cliente1 = sistema.buscar_cliente("CLI-0001")
        cliente2 = sistema.buscar_cliente("CLI-0002")
        servicio1 = sistema.buscar_servicio("SERV-0001")
        servicio2 = sistema.buscar_servicio("SERV-0002")
        servicio3 = sistema.buscar_servicio("SERV-0003")
    except Exception as e:
        print(f"Error al buscar entidades: {e}")
        return
    
    # Reserva 1: Válida - Sala
    try:
        reserva1 = sistema.crear_reserva(
            id_cliente=cliente1.id_cliente,
            id_servicio=servicio1.id_servicio,
            duracion=3,
            num_personas=10,
            requiere_equipamiento=["Proyector", "Audio"],
            descuento=True,
            porcentaje_descuento=15
        )
        print(f"✅ Reserva creada: {reserva1.id_reserva}")
        exitosas += 1
        
        # Confirmar reserva
        detalles = sistema.confirmar_reserva(reserva1.id_reserva)
        print(f"   ✅ Reserva confirmada. Costo total: ${detalles['costo_total']:.2f}")
        
    except Exception as e:
        print(f"❌ Error en reserva 1: {e}")
        fallidas += 1
        operaciones.append(f"❌ Error en reserva 1: {e}")
    
    # Reserva 2: Válida - Equipo
    try:
        reserva2 = sistema.crear_reserva(
            id_cliente=cliente2.id_cliente,
            id_servicio=servicio2.id_servicio,
            duracion=48,
            incluye_seguro=True,
            descuento=10
        )
        print(f"✅ Reserva creada: {reserva2.id_reserva}")
        exitosas += 1
        
        detalles = sistema.confirmar_reserva(reserva2.id_reserva)
        print(f"   ✅ Reserva confirmada. Costo total: ${detalles['costo_total']:.2f}")
        
    except Exception as e:
        print(f"❌ Error en reserva 2: {e}")
        fallidas += 1
        operaciones.append(f"❌ Error en reserva 2: {e}")
    
    # Reserva 3: Válida - Asesoría
    try:
        reserva3 = sistema.crear_reserva(
            id_cliente=cliente1.id_cliente,
            id_servicio=servicio3.id_servicio,
            duracion=4,
            material_incluido=True,
            certificado=True
        )
        print(f"✅ Reserva creada: {reserva3.id_reserva}")
        exitosas += 1
        
        detalles = sistema.confirmar_reserva(reserva3.id_reserva)
        print(f"   ✅ Reserva confirmada. Costo total: ${detalles['costo_total']:.2f}")
        
    except Exception as e:
        print(f"❌ Error en reserva 3: {e}")
        fallidas += 1
        operaciones.append(f"❌ Error en reserva 3: {e}")
    
    # ============================================================
    # 4. RESERVAS INVÁLIDAS (para probar excepciones)
    # ============================================================
    print("\n--- RESERVAS INVÁLIDAS ---")
    
    # Reserva 4: Cliente no existe
    try:
        reserva4 = sistema.crear_reserva(
            id_cliente="CLI-9999",
            id_servicio=servicio1.id_servicio,
            duracion=2
        )
        print("✅ Reserva creada inesperadamente")
    except Exception as e:
        print(f"❌ Error controlado (cliente no existe): {e}")
        fallidas += 1
        operaciones.append(f"❌ Error controlado (cliente no existe): {e}")
    
    # Reserva 5: Servicio no existe
    try:
        reserva5 = sistema.crear_reserva(
            id_cliente=cliente1.id_cliente,
            id_servicio="SERV-9999",
            duracion=2
        )
        print("✅ Reserva creada inesperadamente")
    except Exception as e:
        print(f"❌ Error controlado (servicio no existe): {e}")
        fallidas += 1
        operaciones.append(f"❌ Error controlado (servicio no existe): {e}")
    
    # Reserva 6: Duración inválida
    try:
        reserva6 = sistema.crear_reserva(
            id_cliente=cliente1.id_cliente,
            id_servicio=servicio1.id_servicio,
            duracion=-1
        )
        print("✅ Reserva creada inesperadamente")
    except Exception as e:
        print(f"❌ Error controlado (duración inválida): {e}")
        fallidas += 1
        operaciones.append(f"❌ Error controlado (duración inválida): {e}")
    
    # Reserva 7: Servicio no disponible
    try:
        # Deshabilitar el servicio
        servicio1.cambiar_disponibilidad(False)
        
        reserva7 = sistema.crear_reserva(
            id_cliente=cliente1.id_cliente,
            id_servicio=servicio1.id_servicio,
            duracion=2
        )
        sistema.confirmar_reserva(reserva7.id_reserva)
        print("✅ Reserva creada inesperadamente")
    except Exception as e:
        print(f"❌ Error controlado (servicio no disponible): {e}")
        fallidas += 1
        operaciones.append(f"❌ Error controlado (servicio no disponible): {e}")
    
    # ============================================================
    # 5. CANCELACIÓN DE RESERVAS
    # ============================================================
    print("\n--- CANCELACIÓN DE RESERVAS ---")
    
    try:
        # Cancelar la reserva 2
        resultado = sistema.cancelar_reserva("RES-0002", "Cambio de planes")
        if resultado:
            print("✅ Reserva 2 cancelada exitosamente")
            exitosas += 1
        else:
            print("⚠️ No se pudo cancelar la reserva")
    except Exception as e:
        print(f"❌ Error al cancelar reserva: {e}")
        fallidas += 1
    
    try:
        # Intentar cancelar reserva que no existe
        sistema.cancelar_reserva("RES-9999", "Prueba de error")
    except Exception as e:
        print(f"❌ Error controlado (reserva no existe): {e}")
        fallidas += 1
        operaciones.append(f"❌ Error controlado (reserva no existe): {e}")
    
    # ============================================================
    # 6. ESTADÍSTICAS Y REPORTE FINAL
    # ============================================================
    print("\n" + "="*60)
    print("REPORTE FINAL DEL SISTEMA")
    print("="*60)
    
    estadisticas = sistema.obtener_estadisticas()
    print(f"\n📊 ESTADÍSTICAS DEL SISTEMA:")
    print(f"   - Total clientes: {estadisticas['total_clientes']}")
    print(f"   - Clientes activos: {estadisticas['clientes_activos']}")
    print(f"   - Total servicios: {estadisticas['total_servicios']}")
    print(f"   - Servicios disponibles: {estadisticas['servicios_disponibles']}")
    print(f"   - Total reservas: {estadisticas['total_reservas']}")
    print(f"   - Reservas confirmadas: {estadisticas['reservas_confirmadas']}")
    print(f"   - Reservas pendientes: {estadisticas['reservas_pendientes']}")
    print(f"   - Reservas canceladas: {estadisticas['reservas_canceladas']}")
    
    print(f"\n📋 RESUMEN DE OPERACIONES:")
    print(f"   ✅ Operaciones exitosas: {exitosas}")
    print(f"   ❌ Operaciones fallidas (controladas): {fallidas}")
    print(f"   📝 Total de operaciones: {exitosas + fallidas}")
    
    print("\n📂 Archivo de logs generado en la carpeta 'logs/'")
    print("   - El sistema registra TODOS los errores y eventos importantes")
    print("   - La aplicación nunca se detiene ante errores, manteniendo estabilidad")
    
    print("\n" + "="*60)
    print("SISTEMA ESTABLE Y ROBUSTO - EJECUCIÓN COMPLETA")
    print("="*60)
    
    # Mostrar operaciones detalladas
    print("\n📝 DETALLE DE OPERACIONES:")
    for i, op in enumerate(operaciones, 1):
        print(f"   {i}. {op}")
    
    return sistema

def main():
    """
    Función principal.
    """
    try:
        sistema = simular_operaciones()
        print("\n✅ Simulación completada exitosamente!")
        print("   El sistema ha demostrado manejo robusto de excepciones y estabilidad.")
        
    except Exception as e:
        print(f"\n❌ Error crítico en la simulación: {e}")
        print(traceback.format_exc())
        logger.critical(f"Error crítico en main: {e}")
        sys.exit(1)
    finally:
        print("\n" + "="*60)
        print("FIN DE LA EJECUCIÓN")
        print("="*60)

if __name__ == "__main__":
    main()