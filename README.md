# Sistema de Estadísticas de NiceHash

Sistema en Python para extraer información del pool de minado de NiceHash, incluyendo hashrate, mineros activos y producción mensual.

> 💡 **¿Primera vez aquí?** Lee la [Guía de Inicio Rápido](QUICKSTART.md) (5 minutos)

## 🚀 Características

- **Hashrate en tiempo real**: Visualiza el hashrate de todos tus rigs y dispositivos
- **Mineros activos**: Monitorea cuántos workers están activos por algoritmo
- **Producción mensual**: Obtiene las ganancias de los últimos 30 días
- **Balance no pagado**: Consulta el balance pendiente de pago
- **Estadísticas por algoritmo**: Información detallada de cada algoritmo de minado
- **🆕 Notificaciones Telegram**: Recibe alertas cuando tus rigs se caen o recuperan
- **☁️ GitHub Actions**: Monitor automático en la nube 24/7 sin necesidad de PC encendida

## 📋 Requisitos

- Python 3.7 o superior
- Cuenta de NiceHash con credenciales de API

## 🔧 Instalación

### Opción 1: Instalación Rápida (Recomendada)

Ejecuta el script de instalación automatizado:

```powershell
.\setup.ps1
```

Este script:
- ✅ Verifica que Python esté instalado
- ✅ Instala todas las dependencias
- ✅ Crea el archivo `.env` si no existe
- ✅ Te guía en la configuración

### Opción 2: Instalación Manual

1. **Instala las dependencias**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Configura tus credenciales de API**:
   
   a. Copia el archivo de ejemplo:
   ```powershell
   Copy-Item .env.example .env
   ```
   
   b. Obtén tus credenciales de NiceHash:
      - **Lee la guía detallada**: [CONFIGURACION_API.md](CONFIGURACION_API.md)
      - Ve a https://www.nicehash.com/my/settings/keys
      - Haz clic en "Create New API Key"
      - Asigna un nombre (ej: "Mining Stats")
      - Selecciona el permiso: ✅ **VMDS** (View mining data and statistics)
      - Copia el API Key, API Secret y Organization ID
   
   c. Edita el archivo `.env` con tus credenciales:
   ```
   NICEHASH_API_KEY=tu-api-key-aqui
   NICEHASH_API_SECRET=tu-api-secret-aqui
   NICEHASH_ORG_ID=tu-organization-id-aqui
   NICEHASH_API_URL=https://api2.nicehash.com
   ```
   
   📖 **Para instrucciones detalladas paso a paso, consulta: [CONFIGURACION_API.md](CONFIGURACION_API.md)**

## 🎯 Uso

### Script Principal (Visualización en Consola)

Ejecuta el script principal para ver las estadísticas en la consola:

```powershell
python main.py
```

El script mostrará:

1. **Información de Rigs y Hashrate**
   - Total de rigs configurados
   - Rigs activos/inactivos
   - Hashrate por dispositivo y algoritmo

2. **Workers Activos en el Mes**
   - Número total de workers activos
   - Desglose por algoritmo

3. **Estadísticas por Algoritmo**
   - Hashrate aceptado y rechazado
   - Balance no pagado por algoritmo

4. **Producción del Último Mes**
   - Ganancias diarias (últimos 10 días)
   - Total de profitabilidad del mes
   - Revenue total

5. **Balance No Pagado**
   - Balance total pendiente de pago
   - Desglose por algoritmo

### Script de Exportación (JSON)

Para exportar todas las estadísticas a un archivo JSON:

```powershell
# Exportar con nombre por defecto (nicehash_stats.json)
python export_stats.py

# Exportar con nombre personalizado
python export_stats.py mi_reporte.json

# Ver resumen de un archivo exportado
python export_stats.py summary
python export_stats.py summary mi_reporte.json
```

El archivo JSON incluye:
- Información completa de todos los rigs
- Workers activos por algoritmo
- Estadísticas detalladas por algoritmo
- Producción diaria de los últimos 30 días
- Balance no pagado

Este formato es ideal para:
- Análisis posterior con otras herramientas
- Integración con sistemas de monitoreo
- Guardar histórico de estadísticas
- Procesamiento automatizado de datos

### Ejemplos Avanzados

Para ver ejemplos de uso avanzado del cliente:

```powershell
python advanced_example.py
```

Incluye funciones para:
- 📊 Calcular rentabilidad promedio y proyecciones
- ⚠️ Alertar sobre rigs inactivos
- 🔄 Comparar rendimiento entre algoritmos
- 🏆 Encontrar el mejor día de producción del mes
- ⚡ Monitorear hashrate y tasas de rechazo

Puedes usar estas funciones como base para crear tus propios scripts personalizados.

## 📁 Estructura del Proyecto

```
Nicehash/
│
├── main.py                 # Script principal (visualización)
├── export_stats.py         # Script de exportación a JSON
├── advanced_example.py     # Ejemplos de uso avanzado
├── nicehash_client.py      # Cliente de la API de NiceHash
├── config.py               # Configuración y validación
├── setup.ps1              # Script de instalación automática (Windows)
├── requirements.txt        # Dependencias de Python
├── .env.example           # Plantilla de configuración
├── .env                   # Tu configuración (no compartir)
├── .gitignore             # Archivos a ignorar en git
└── README.md              # Esta documentación
```

## 🔐 Seguridad

- **NUNCA** compartas tu archivo `.env` o tus credenciales de API
- El `.env` contiene información sensible (API Key y Secret)
- Mantén tus permisos de API al mínimo necesario
- Para este proyecto solo necesitas el permiso **VMDS** (View mining data and statistics)

## 🛠️ Personalización

### Modificar el período de producción

En [main.py](main.py), función `show_monthly_production()`, puedes cambiar:

```python
# Cambiar de 30 a 60 días, por ejemplo
from_date = to_date - timedelta(days=60)
```

### Agregar más estadísticas

El cliente `NiceHashClient` incluye métodos adicionales:

```python
# Obtener información de pagos
payouts = client.get_payouts()

# Obtener dirección de minería
address = client.get_mining_address()
```

### Automatizar la exportación

Puedes crear un script de PowerShell para exportaciones automáticas:

```powershell
# Archivo: exportar_diario.ps1
$fecha = Get-Date -Format "yyyy-MM-dd"
python export_stats.py "reportes\stats_$fecha.json"
```

Y programarlo con el Programador de Tareas de Windows para ejecutarlo diariamente.

## 📊 Ejemplo de Salida

```
╔══════════════════════════════════════════════════════════╗
║          NICEHASH MINING STATISTICS                      ║
╚══════════════════════════════════════════════════════════╝

✓ Cliente inicializado correctamente

============================================================
  INFORMACIÓN DE RIGS Y HASHRATE
============================================================

📊 Total de Rigs: 2
✅ Rigs Activos: 2
❌ Rigs Inactivos: 0

------------------------------------------------------------
Detalle de Rigs:
------------------------------------------------------------

✅ Rig Principal
   Estado: MINING
   └─ NVIDIA RTX 3080 (DAGGERHASHIMOTO): 95.23 MH/s

✅ Rig Secundario
   Estado: MINING
   └─ AMD RX 6800 (DAGGERHASHIMOTO): 62.15 MH/s

============================================================
  PRODUCCIÓN DEL ÚLTIMO MES
============================================================

📅 Período: 21/12/2025 - 21/01/2026
------------------------------------------------------------

Ganancias diarias (últimos 10 días):
------------------------------------------------------------
  2026-01-12: 0.00012345 BTC (Revenue: 0.00012500 BTC)
  2026-01-13: 0.00011890 BTC (Revenue: 0.00012100 BTC)
  ...

============================================================
💰 Total del mes (últimos 30 días):
   Profitabilidad: 0.00350000 BTC
   Revenue: 0.00360000 BTC
============================================================
```

## 🐛 Solución de Problemas

### Error: "NICEHASH_API_KEY no está configurada"

- Asegúrate de haber creado el archivo `.env` (copia de `.env.example`)
- Verifica que las credenciales estén correctamente configuradas

### Error de autenticación (401)

- Verifica que tu API Key y Secret sean correctos
- Asegúrate de que el Organization ID sea correcto
- Verifica que la API Key tenga los permisos necesarios (VMDS)

### Error: "ModuleNotFoundError"

- Instala las dependencias: `pip install -r requirements.txt`

## � Monitor de Rigs con Telegram

### ¿Qué es?

El monitor de Telegram te envía notificaciones automáticas cuando:
- 🔴 Un rig se cae o deja de minar
- ✅ Un rig se recupera y vuelve a minar
- 📊 Reportes periódicos del estado de todos tus rigs

### Configuración Rápida

1. **Configura tu bot de Telegram**:
   ```powershell
   # Lee la guía completa
   notepad TELEGRAM_SETUP.md
   ```
   - Crea un bot con @BotFather
   - Obtén tu Token y Chat ID
   - Agrégalos a tu archivo .env

2. **Prueba la configuración**:
   ```powershell
   python test_telegram.py
   ```

3. **Ejecuta el monitor localmente**:
   ```powershell
   # Monitor continuo (deja la ventana abierta)
   python telegram_bot.py
   
   # Verificación única
   python telegram_bot.py --check-once
   ```

### 🌐 Monitor Automático con GitHub Actions

¿Quieres monitorear tus rigs 24/7 sin tener tu PC encendida? Usa GitHub Actions (gratis):

1. **Lee la guía completa**:
   ```powershell
   notepad GITHUB_ACTIONS_SETUP.md
   ```

2. **Configuración rápida**:
   - Sube tu código a GitHub
   - Configura 5 secrets en Settings → Secrets and variables → Actions
   - ¡Listo! GitHub verificará tus rigs cada 5 minutos automáticamente

3. **Ventajas**:
   - ☁️ Funciona en la nube (no necesitas tu PC)
   - 🆓 Gratis (2,000 minutos/mes)
   - 📱 Notificaciones en Telegram
   - 🔄 Monitoreo automático 24/7

### 📚 Documentación Completa

- **[TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)** - Configurar bot de Telegram paso a paso
- **[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)** - Configurar monitor automático en la nube

## �📚 Documentación de la API

- [Documentación oficial de NiceHash API](https://www.nicehash.com/docs/)
- [Miner Private Endpoints](https://www.nicehash.com/docs/rest/-miner-private)

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún bug o quieres agregar una nueva característica, no dudes en crear un issue o pull request.

## ⚠️ Disclaimer

Este software se proporciona "tal cual", sin garantías de ningún tipo. Úsalo bajo tu propio riesgo. El autor no se hace responsable de ningún daño o pérdida que pueda resultar del uso de este software.
