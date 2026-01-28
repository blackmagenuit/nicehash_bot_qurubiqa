# 📊 Sistema de Estadísticas de NiceHash - Resumen del Proyecto

## 🎯 Objetivo

Extraer y visualizar información del pool de minado de NiceHash mediante su API REST, incluyendo:
- Hashrate en tiempo real
- Mineros activos
- Producción mensual
- Balance no pagado
- Estadísticas por algoritmo

## 📁 Estructura del Proyecto

```
Nicehash/
│
├── 📖 Documentación
│   ├── README.md                    # Documentación principal completa
│   ├── QUICKSTART.md               # Guía de inicio rápido (5 min)
│   └── CONFIGURACION_API.md        # Guía detallada de configuración de API
│
├── 🔧 Configuración
│   ├── .env                        # Credenciales (NO COMPARTIR)
│   ├── .env.example               # Plantilla de configuración
│   ├── .gitignore                 # Archivos a ignorar en git
│   ├── config.py                  # Manejo de configuración
│   └── requirements.txt           # Dependencias de Python
│
├── ⚙️ Core del Sistema
│   └── nicehash_client.py         # Cliente de la API con autenticación HMAC-SHA256
│
├── 🚀 Scripts de Usuario
│   ├── main.py                    # Visualización en consola (principal)
│   ├── export_stats.py            # Exportación a JSON
│   ├── advanced_example.py        # Ejemplos de uso avanzado
│   └── test_config.py             # Test de configuración
│
└── 🛠️ Utilidades
    ├── setup.ps1                  # Instalación automática (Windows)
    └── exportar_diario.ps1        # Script para exportación programada
```

## 🔑 Archivos Principales

### Core

| Archivo | Descripción | Líneas |
|---------|-------------|--------|
| `nicehash_client.py` | Cliente completo de la API con autenticación HMAC-SHA256 y métodos para todos los endpoints | ~200 |
| `config.py` | Gestión de configuración y validación de credenciales | ~25 |

### Scripts de Usuario

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `main.py` | Visualiza estadísticas en consola con formato bonito | `python main.py` |
| `export_stats.py` | Exporta todas las estadísticas a JSON | `python export_stats.py` |
| `advanced_example.py` | Ejemplos avanzados (alertas, proyecciones, análisis) | `python advanced_example.py` |
| `test_config.py` | Verifica que la configuración sea correcta | `python test_config.py` |

### Utilidades

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `setup.ps1` | Instalación automatizada para Windows | `.\setup.ps1` |
| `exportar_diario.ps1` | Script para programar exportaciones automáticas | Programador de Tareas |

## 🔌 API de NiceHash

### Endpoints Implementados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `get_rigs()` | `/main/api/v2/mining/rigs` | Información de todos los rigs |
| `get_active_workers()` | `/main/api/v2/mining/rigs/activeWorkers` | Workers activos por algoritmo |
| `get_rig_stats_algo()` | `/main/api/v2/mining/rigs/stats/algo` | Estadísticas por algoritmo |
| `get_daily_earnings()` | `/main/api/v2/mining/rigs/stats/data` | Ganancias diarias |
| `get_algo_stats()` | `/main/api/v2/mining/algo/stats` | Estadísticas generales de algoritmos |
| `get_payouts()` | `/main/api/v2/mining/rigs/payouts` | Información de pagos |
| `get_mining_address()` | `/main/api/v2/mining/miningAddress` | Dirección de minería |
| `get_unpaid_stats()` | `/main/api/v2/mining/rig/stats/unpaid` | Balance no pagado |

### Autenticación

Implementa el sistema de autenticación HMAC-SHA256 de NiceHash:

```
HMAC-SHA256(
    API_KEY || timestamp || nonce || "" || ORG_ID || "" || 
    METHOD || PATH || QUERY || BODY,
    API_SECRET
)
```

Headers requeridos:
- `X-Time`: Timestamp UTC en milisegundos
- `X-Nonce`: UUID único por petición
- `X-Organization-Id`: Organization ID
- `X-Request-Id`: UUID único de la petición
- `X-Auth`: API_KEY:SIGNATURE

## 📊 Funcionalidades

### 1. Visualización en Consola (main.py)

- **Rigs y Hashrate**
  - Total de rigs configurados
  - Rigs activos vs inactivos
  - Hashrate por dispositivo y algoritmo
  
- **Workers Activos**
  - Total de workers activos
  - Desglose por algoritmo
  
- **Estadísticas por Algoritmo**
  - Hashrate aceptado y rechazado
  - Balance no pagado
  
- **Producción del Mes**
  - Últimos 30 días de ganancias
  - Total y promedio diario
  
- **Balance No Pagado**
  - Balance total pendiente
  - Desglose por algoritmo

### 2. Exportación a JSON (export_stats.py)

Exporta toda la información a un archivo JSON estructurado:

```json
{
  "timestamp": "2026-01-21T10:30:00",
  "rigs": { ... },
  "active_workers": { ... },
  "algo_statistics": { ... },
  "monthly_production": { ... },
  "unpaid_balance": { ... }
}
```

### 3. Ejemplos Avanzados (advanced_example.py)

- Cálculo de rentabilidad promedio y proyecciones
- Alertas de rigs inactivos
- Comparación de algoritmos
- Identificación del mejor día de producción
- Monitoreo de hashrate y tasas de rechazo

## 🔒 Seguridad

### Permisos Necesarios

Solo requiere el permiso **VMDS** (View Mining Data and Statistics):
- ✅ Lectura de datos de minería
- ❌ NO puede retirar fondos
- ❌ NO puede modificar configuración
- ❌ NO puede crear/cancelar órdenes

### Protección de Credenciales

- `.env` en `.gitignore` (no se sube a git)
- Credenciales nunca en el código
- Carga desde variables de entorno
- Validación antes de uso

## 🚀 Flujo de Uso Recomendado

```
1. Instalación
   ├─> .\setup.ps1
   │
2. Configuración
   ├─> Crear API Key en NiceHash
   ├─> Copiar credenciales a .env
   │
3. Verificación
   ├─> python test_config.py
   │
4. Uso Regular
   ├─> python main.py           (ver en consola)
   ├─> python export_stats.py   (exportar datos)
   └─> python advanced_example.py (análisis avanzado)
   
5. Automatización (Opcional)
   └─> Programar exportar_diario.ps1 con Programador de Tareas
```

## 📦 Dependencias

```
requests>=2.31.0      # HTTP client
python-dotenv>=1.0.0  # Gestión de .env
```

Ambas son librerías estándar y confiables en el ecosistema Python.

## 🎨 Características del Código

### Buenas Prácticas

- ✅ Type hints en funciones
- ✅ Docstrings completos
- ✅ Manejo de errores robusto
- ✅ Código modular y reutilizable
- ✅ Separación de responsabilidades
- ✅ Configuración externa (.env)
- ✅ Sin credenciales hardcodeadas

### Arquitectura

```
┌─────────────────┐
│   Scripts       │  main.py, export_stats.py, etc.
│   de Usuario    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  NiceHashClient │  nicehash_client.py
│     (Core)      │  • Autenticación HMAC-SHA256
└────────┬────────┘  • Métodos de API
         │           • Gestión de peticiones
         │
         ▼
┌─────────────────┐
│   Config        │  config.py
│                 │  • Carga de .env
└─────────────────┘  • Validación
```

## 📈 Casos de Uso

1. **Monitoreo Diario**: Ejecutar `main.py` cada mañana para revisar el estado
2. **Análisis Histórico**: Usar `export_stats.py` + Programador de Tareas para mantener histórico
3. **Alertas Personalizadas**: Modificar `advanced_example.py` para crear alertas por email/Telegram
4. **Dashboard**: Usar JSON exportado para crear visualizaciones en otras herramientas
5. **Análisis de Rentabilidad**: Comparar producción entre diferentes períodos

## 🔧 Personalización

El código está diseñado para ser fácilmente extensible:

### Agregar Nuevos Endpoints

```python
# En nicehash_client.py
def get_nuevo_endpoint(self) -> Dict:
    return self._make_request('GET', '/main/api/v2/nuevo/endpoint')
```

### Crear Alertas Personalizadas

```python
# Basado en advanced_example.py
def alerta_hashrate_bajo():
    if hashrate < umbral:
        enviar_notificacion()
```

### Integrar con Otras Herramientas

El JSON exportado es compatible con:
- Power BI
- Tableau
- Grafana
- Excel / Google Sheets
- Scripts personalizados

## 📚 Recursos Adicionales

- **Documentación de NiceHash API**: https://www.nicehash.com/docs/
- **Repositorio de ejemplos oficiales**: https://github.com/nicehash/rest-clients-demo
- **Soporte de NiceHash**: https://www.nicehash.com/support

## ✅ Checklist de Implementación

- [x] Cliente de API con autenticación HMAC-SHA256
- [x] Gestión segura de credenciales
- [x] Script de visualización en consola
- [x] Exportación a JSON
- [x] Ejemplos avanzados de uso
- [x] Test de configuración
- [x] Script de instalación automática
- [x] Script de automatización
- [x] Documentación completa
- [x] Guía de inicio rápido
- [x] Guía de configuración de API
- [x] Manejo robusto de errores
- [x] .gitignore para proteger credenciales

## 🎉 Estado del Proyecto

**Estado**: ✅ Completo y listo para usar

**Versión**: 1.0

**Fecha**: Enero 2026

**Compatibilidad**: Windows con PowerShell, Python 3.7+

---

**Desarrollado para facilitar el monitoreo de operaciones de minado en NiceHash** 🚀
