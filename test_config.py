"""
Script de prueba para verificar la configuración de NiceHash
Ejecuta este script para asegurarte de que todo está correctamente configurado
"""
import sys
from nicehash_client import NiceHashClient


def test_configuration():
    """Prueba la configuración y conexión con NiceHash"""
    
    print("\n╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "TEST DE CONFIGURACION" + " " * 25 + "║")
    print("╚" + "═" * 58 + "╝\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Verificar archivo .env
    print("Test 1: Verificando archivo .env...")
    try:
        import config
        print("  ✓ Archivo .env encontrado")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Error: {e}")
        tests_failed += 1
        return
    
    # Test 2: Verificar credenciales configuradas
    print("\nTest 2: Verificando credenciales...")
    try:
        config.validate_config()
        print("  ✓ Credenciales configuradas")
        tests_passed += 1
    except ValueError as e:
        print(f"  ✗ {e}")
        print("\n💡 Solución:")
        print("   1. Edita el archivo .env")
        print("   2. Agrega tus credenciales de NiceHash")
        print("   3. Consulta CONFIGURACION_API.md para ayuda")
        tests_failed += 1
        return
    
    # Test 3: Verificar módulos instalados
    print("\nTest 3: Verificando módulos de Python...")
    try:
        import requests
        import dotenv
        print("  ✓ Módulos instalados correctamente")
        tests_passed += 1
    except ImportError as e:
        print(f"  ✗ Error: {e}")
        print("\n💡 Solución:")
        print("   pip install -r requirements.txt")
        tests_failed += 1
        return
    
    # Test 4: Intentar conectar con la API
    print("\nTest 4: Probando conexión con NiceHash API...")
    try:
        client = NiceHashClient()
        print("  ✓ Cliente inicializado")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Error al inicializar cliente: {e}")
        tests_failed += 1
        return
    
    # Test 5: Obtener datos de prueba
    print("\nTest 5: Obteniendo datos de prueba...")
    try:
        # Intentar obtener información de balance
        account_info = client.get_account_info()
        print("  ✓ Conexión exitosa con la API")
        tests_passed += 1
        
        # Mostrar información de la cuenta
        if 'total' in account_info and 'totalBalance' in account_info['total']:
            balance = account_info['total']['totalBalance']
            currency = account_info['total']['currency']
            print(f"  ℹ️  Balance total: {balance} {currency}")
        
        # Mostrar Organization ID
        import config
        print(f"  ℹ️  Organization ID: {config.ORG_ID}")
    except Exception as e:
        print(f"  ✗ Error al conectar con la API: {e}")
        print("\n💡 Posibles causas:")
        print("   • API Key incorrecta")
        print("   • API Secret incorrecta")
        print("   • Organization ID incorrecta")
        print("   • La API Key no tiene el permiso VMDS")
        print("\n💡 Solución:")
        print("   1. Verifica tus credenciales en el archivo .env")
        print("   2. Consulta CONFIGURACION_API.md para ayuda")
        tests_failed += 1
        return
    
    # Test 6: Verificar permisos
    print("\nTest 6: Verificando permisos de la API Key...")
    try:
        # Intentar obtener estadísticas (requiere permiso VMDS)
        rigs = client.get_rigs()
        print("  ✓ Permiso VMDS confirmado")
        tests_passed += 1
        
        # Mostrar información básica
        if 'miningRigs' in rigs:
            num_rigs = len(rigs['miningRigs'])
            print(f"  ℹ️  Rigs encontrados: {num_rigs}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n💡 Posible causa:")
        print("   • La API Key no tiene el permiso VMDS")
        print("\n💡 Solución:")
        print("   1. Ve a https://www.nicehash.com/my/settings/keys")
        print("   2. Verifica que tu API Key tenga el permiso:")
        print("      ✅ VMDS - View mining data and statistics")
        print("   3. Si no lo tiene, crea una nueva API Key con ese permiso")
        tests_failed += 1
        return
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Tests exitosos: {tests_passed}/6")
    print(f"Tests fallidos: {tests_failed}/6")
    
    if tests_failed == 0:
        print("\n🎉 ¡CONFIGURACIÓN CORRECTA!")
        print("\n✅ Todo está listo para usar el sistema")
        print("\n🚀 Comandos disponibles:")
        print("   python main.py           - Ver estadísticas en consola")
        print("   python export_stats.py   - Exportar a JSON")
        print("   python advanced_example.py - Ver ejemplos avanzados")
    else:
        print("\n❌ HAY ERRORES EN LA CONFIGURACIÓN")
        print("\n📖 Consulta estos recursos:")
        print("   • CONFIGURACION_API.md - Guía paso a paso")
        print("   • QUICKSTART.md - Inicio rápido")
        print("   • README.md - Documentación completa")
    
    print("\n" + "=" * 60 + "\n")
    
    return tests_failed == 0


if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)
