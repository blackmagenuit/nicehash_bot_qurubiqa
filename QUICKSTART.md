# ⚡ Quick Start - NiceHash Stats

Guía rápida de 5 minutos para empezar a usar el sistema.

## 🚀 Inicio Rápido

### 1. Instalar (2 minutos)

```powershell
# Ejecuta el script de instalación
.\setup.ps1
```

### 2. Configurar (2 minutos)

1. Ve a: https://www.nicehash.com/my/settings/keys
2. Crea una nueva API Key con permiso **VMDS**
3. Copia tus credenciales en el archivo `.env`

### 3. Ejecutar (1 minuto)

```powershell
# Primero, prueba tu configuración
python test_config.py

# Si todo está OK, ver estadísticas en consola
python main.py

# Exportar a JSON
python export_stats.py

# Ver ejemplos avanzados
python advanced_example.py
```

## 📝 ¿Primera vez con APIs?

Lee la guía completa: [CONFIGURACION_API.md](CONFIGURACION_API.md)

## ❓ ¿Problemas?

### Error: "NICEHASH_API_KEY no está configurada"
- Verifica que el archivo `.env` existe y tiene tus credenciales

### Error 401: "Unauthorized"
- Verifica que copiaste correctamente API Key, Secret y Organization ID
- Asegúrate de que la API Key tenga el permiso VMDS

### Error: "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

## 📚 Documentación Completa

- **Guía completa**: [README.md](README.md)
- **Configuración de API**: [CONFIGURACION_API.md](CONFIGURACION_API.md)
- **Ejemplos de código**: Ver [advanced_example.py](advanced_example.py)

## 🎯 Lo que obtendrás

- ⚡ **Hashrate actual** de todos tus rigs
- 👷 **Workers activos** por algoritmo
- 💰 **Producción del mes** en BTC
- 💵 **Balance no pagado** actual
- 📊 **Estadísticas por algoritmo**

---

**Tiempo total**: ~5 minutos ⏱️

**Dificultad**: Principiante 👶

**¿Listo?** ¡Empieza con `.\setup.ps1`! 🚀
