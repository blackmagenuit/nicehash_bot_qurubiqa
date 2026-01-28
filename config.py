"""
Configuración para el cliente de NiceHash
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de API
API_KEY = os.getenv('NICEHASH_API_KEY')
API_SECRET = os.getenv('NICEHASH_API_SECRET')
ORG_ID = os.getenv('NICEHASH_ORG_ID')
API_URL = os.getenv('NICEHASH_API_URL', 'https://api2.nicehash.com')

# Configuración de Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def validate_config():
    """Valida que todas las configuraciones necesarias estén presentes"""
    if not API_KEY:
        raise ValueError("NICEHASH_API_KEY no está configurada en el archivo .env")
    if not API_SECRET:
        raise ValueError("NICEHASH_API_SECRET no está configurada en el archivo .env")
    if not ORG_ID:
        raise ValueError("NICEHASH_ORG_ID no está configurada en el archivo .env")
    return True
