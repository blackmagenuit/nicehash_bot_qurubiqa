# Configuración del Bot de Telegram

Esta guía te ayudará a configurar el bot de Telegram para recibir notificaciones cuando tus rigs se caigan o se recuperen.

## 📋 Requisitos Previos

- Cuenta de Telegram
- Las credenciales de NiceHash ya configuradas en `.env`

## 🤖 Paso 1: Crear el Bot de Telegram

1. **Abre Telegram** y busca el bot oficial: `@BotFather`

2. **Inicia una conversación** con BotFather y envía el comando:
   ```
   /newbot
   ```

3. **Sigue las instrucciones**:
   - Elige un nombre para tu bot (ej: "NiceHash Monitor")
   - Elige un username para tu bot (debe terminar en "bot", ej: "minicehash_monitor_bot")

4. **Copia el token** que te proporciona BotFather. Se verá así:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

5. **Guarda este token**, lo necesitarás en el siguiente paso.

## 💬 Paso 2: Obtener tu Chat ID

### Opción A: Método Automático (Recomendado)

1. **Busca tu bot** en Telegram usando el username que elegiste

2. **Inicia la conversación** con tu bot haciendo clic en "Start" o enviando:
   ```
   /start
   ```

3. **Abre tu navegador** y ve a esta URL (reemplaza `<TOKEN>` con tu token):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   
   Ejemplo:
   ```
   https://api.telegram.org/bot1234567890:ABCdefGHIjklMNOpqrsTUVwxyz/getUpdates
   ```

4. **Busca tu Chat ID** en la respuesta JSON. Aparecerá así:
   ```json
   {
     "ok": true,
     "result": [
       {
         "update_id": 123456789,
         "message": {
           "message_id": 1,
           "from": {...},
           "chat": {
             "id": 987654321,  ← Este es tu CHAT_ID
             "type": "private"
           }
         }
       }
     ]
   }
   ```

5. **Copia el número** que aparece en `"id":` dentro de `"chat":`

### Opción B: Usando otro Bot

1. Busca en Telegram: `@userinfobot`
2. Envíale el comando `/start`
3. Te responderá con tu Chat ID

## ⚙️ Paso 3: Configurar las Credenciales

1. **Abre el archivo** `.env` en tu editor

2. **Añade tus credenciales de Telegram**:
   ```env
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=987654321
   ```

3. **Guarda el archivo**

## 🚀 Paso 4: Ejecutar el Bot

1. **Ejecuta el monitor de Telegram**:
   ```powershell
   python telegram_bot.py
   ```

2. **Verifica que funcione**:
   - Deberías recibir un mensaje en Telegram indicando que el bot está activo
   - El monitor comenzará a verificar tus rigs cada minuto
   - Recibirás notificaciones cuando un rig cambie de estado

## 📊 Funcionalidades del Bot

### Notificaciones Automáticas

El bot te notificará automáticamente cuando:

- ✅ **Un rig se recupera** (vuelve a minar)
- 🔴 **Un rig se cae** (deja de minar)

### Reportes Periódicos

Cada hora recibirás un reporte con:
- Total de rigs
- Rigs activos
- Rigs caídos
- Lista de rigs offline (si hay)

### Intervalo de Verificación

Por defecto, el bot verifica el estado cada **60 segundos**. Puedes modificar esto editando la variable `CHECK_INTERVAL` en `telegram_bot.py`.

## 🛠️ Personalización

### Cambiar el intervalo de verificación

Edita el archivo `telegram_bot.py` y modifica:

```python
CHECK_INTERVAL = 60  # Segundos entre verificaciones
```

### Cambiar el intervalo de reportes

```python
REPORT_INTERVAL = 3600  # Segundos entre reportes (1 hora)
```

## 🔍 Solución de Problemas

### No recibo mensajes del bot

1. **Verifica las credenciales** en `.env`:
   - El `TELEGRAM_BOT_TOKEN` debe ser correcto
   - El `TELEGRAM_CHAT_ID` debe ser tu ID personal

2. **Asegúrate de haber iniciado** conversación con tu bot en Telegram

3. **Revisa la consola** donde ejecutaste el bot para ver si hay errores

### El bot se detiene solo

1. **Mantén la ventana de PowerShell abierta** mientras el bot esté activo
2. Para ejecutar el bot en segundo plano, considera usar una herramienta como `pm2` o un servicio de Windows

### Quiero ejecutar el bot 24/7

Considera estas opciones:

1. **Servidor/VPS**: Ejecuta el bot en un servidor Linux con `screen` o `tmux`
2. **Servicio de Windows**: Configura el script como un servicio
3. **Planificador de tareas**: Usa el Programador de tareas de Windows

## 📝 Ejemplo de Notificaciones

### Cuando un rig se cae:
```
🔴 Alerta: Rig Caído

🖥️ Rig: 10x1x0x123
📊 Estado: CAÍDO
🕐 Hora: 2026-01-27 15:30:45

⚠️ El rig dejó de minar
```

### Cuando un rig se recupera:
```
✅ Rig Recuperado

🖥️ Rig: 10x1x0x123
📊 Estado: ACTIVO
🕐 Hora: 2026-01-27 15:35:12

✅ El rig ha vuelto a minar correctamente
```

### Reporte periódico:
```
📊 Reporte de Estado de Rigs

🕐 Hora: 2026-01-27 16:00:00

📈 Total de Rigs: 25
✅ Activos: 24
❌ Offline: 1

🔴 Rigs Caídos:
  • 10x1x0x107
```

## ⚡ Comandos Útiles

Para detener el bot:
```
Presiona Ctrl+C en la ventana donde está corriendo
```

Para ver el log en tiempo real mientras corre en segundo plano, redirige la salida:
```powershell
python telegram_bot.py > telegram_bot.log 2>&1
```

## 🆘 Soporte

Si tienes problemas:
1. Revisa que todas las credenciales en `.env` sean correctas
2. Verifica que el bot de Telegram esté activo (búscalo en Telegram)
3. Asegúrate de haber iniciado conversación con el bot
4. Revisa los mensajes de error en la consola
