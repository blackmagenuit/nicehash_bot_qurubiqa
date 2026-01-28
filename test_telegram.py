"""
Script de prueba para verificar la configuración de Telegram
Ejecuta este script para asegurarte de que Telegram está correctamente configurado
"""
import sys
import config


def test_telegram_config():
    """Prueba la configuración de Telegram"""
    
    print("\n╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "TEST DE TELEGRAM" + " " * 30 + "║")
    print("╚" + "═" * 58 + "╝\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Verificar que las credenciales de Telegram estén configuradas
    print("Test 1: Verificando credenciales de Telegram en .env...")
    try:
        if not config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN no está configurado en .env")
        if not config.TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID no está configurado en .env")
        
        print("  ✓ TELEGRAM_BOT_TOKEN configurado")
        print("  ✓ TELEGRAM_CHAT_ID configurado")
        tests_passed += 1
    except ValueError as e:
        print(f"  ✗ {e}")
        print("\n💡 Solución:")
        print("   1. Edita el archivo .env")
        print("   2. Agrega:")
        print("      TELEGRAM_BOT_TOKEN=tu_token_aqui")
        print("      TELEGRAM_CHAT_ID=tu_chat_id_aqui")
        print("   3. Consulta TELEGRAM_SETUP.md para obtener estos valores")
        tests_failed += 1
        return False
    
    # Test 2: Verificar formato del token
    print("\nTest 2: Verificando formato del token...")
    try:
        token = config.TELEGRAM_BOT_TOKEN
        if ':' not in token or len(token) < 30:
            raise ValueError("El formato del token parece incorrecto")
        
        print(f"  ✓ Formato del token correcto")
        print(f"  ℹ️  Token: {token[:10]}...{token[-5:]}")
        tests_passed += 1
    except ValueError as e:
        print(f"  ✗ {e}")
        print("\n💡 El token debe tener el formato:")
        print("   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
        tests_failed += 1
    
    # Test 3: Verificar formato del Chat ID
    print("\nTest 3: Verificando formato del Chat ID...")
    try:
        chat_id = config.TELEGRAM_CHAT_ID
        # El Chat ID debe ser numérico (puede ser negativo para grupos)
        if not chat_id or not (chat_id.lstrip('-').isdigit()):
            raise ValueError("El formato del Chat ID parece incorrecto")
        
        print(f"  ✓ Formato del Chat ID correcto")
        print(f"  ℹ️  Chat ID: {chat_id}")
        tests_passed += 1
    except ValueError as e:
        print(f"  ✗ {e}")
        print("\n💡 El Chat ID debe ser un número:")
        print("   Ejemplo: 987654321 o -987654321")
        tests_failed += 1
    
    # Test 4: Probar conexión con Telegram
    print("\nTest 4: Probando conexión con Telegram...")
    try:
        from telegram_bot import TelegramNotifier
        
        notifier = TelegramNotifier(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        print("  ✓ Notificador inicializado")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Error al inicializar: {e}")
        tests_failed += 1
        return False
    
    # Test 5: Enviar mensaje de prueba
    print("\nTest 5: Enviando mensaje de prueba...")
    try:
        test_message = "🧪 <b>Mensaje de Prueba</b>\n\n"
        test_message += "✅ Si recibes este mensaje, tu bot de Telegram está correctamente configurado!\n\n"
        test_message += "🎉 Ya puedes usar el monitor de rigs con Telegram"
        
        success = notifier.send_message(test_message)
        
        if success:
            print("  ✓ Mensaje enviado correctamente")
            print("  ℹ️  Revisa tu chat de Telegram!")
            tests_passed += 1
        else:
            raise Exception("No se pudo enviar el mensaje")
            
    except Exception as e:
        print(f"  ✗ Error al enviar mensaje: {e}")
        print("\n💡 Posibles causas:")
        print("   • El token del bot es incorrecto")
        print("   • El Chat ID es incorrecto")
        print("   • No has iniciado conversación con el bot")
        print("\n💡 Solución:")
        print("   1. Ve a Telegram y busca tu bot")
        print("   2. Haz clic en 'Start' o envía /start")
        print("   3. Vuelve a ejecutar este test")
        tests_failed += 1
        return False
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Tests exitosos: {tests_passed}/5")
    print(f"Tests fallidos: {tests_failed}/5")
    
    if tests_failed == 0:
        print("\n🎉 ¡TELEGRAM CONFIGURADO CORRECTAMENTE!")
        print("\n✅ Todo está listo para usar el monitor con Telegram")
        print("\n🚀 Comandos disponibles:")
        print("   python telegram_bot.py          - Ejecutar monitor continuo")
        print("   python telegram_bot.py --check-once - Verificación única")
        print("\n📚 Siguiente paso:")
        print("   Consulta GITHUB_ACTIONS_SETUP.md para configurar")
        print("   el monitor automático en la nube con GitHub Actions")
    else:
        print("\n❌ HAY ERRORES EN LA CONFIGURACIÓN DE TELEGRAM")
        print("\n📖 Consulta estos recursos:")
        print("   • TELEGRAM_SETUP.md - Guía completa de Telegram")
        print("   • README.md - Documentación general")
    
    print("\n" + "=" * 60 + "\n")
    
    return tests_failed == 0


if __name__ == "__main__":
    success = test_telegram_config()
    sys.exit(0 if success else 1)
