# Configuración de GitHub Actions con Telegram

Esta guía te mostrará cómo configurar GitHub Actions para monitorear tus rigs automáticamente en la nube y recibir notificaciones en Telegram.

## 📋 ¿Qué es GitHub Actions?

GitHub Actions permite ejecutar código automáticamente en los servidores de GitHub. En este caso, se ejecutará el monitor de rigs cada 5 minutos sin necesidad de tener tu computadora encendida.

## ✅ Ventajas de usar GitHub Actions

- ✨ **Gratis**: GitHub ofrece 2,000 minutos gratis al mes
- ☁️ **En la nube**: No necesitas tu PC encendida
- 🔄 **Automático**: Se ejecuta cada 5 minutos
- 📱 **Notificaciones**: Recibes alertas en Telegram cuando un rig se cae o recupera

## 🚀 Pasos para Configurar

### Paso 1: Configurar Telegram

Primero necesitas configurar tu bot de Telegram. Sigue la guía [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) para:

1. Crear tu bot de Telegram con BotFather
2. Obtener tu `TELEGRAM_BOT_TOKEN`
3. Obtener tu `TELEGRAM_CHAT_ID`

**Guarda estos valores**, los necesitarás en el siguiente paso.

### Paso 2: Configurar Secrets en GitHub

Los "secrets" son variables seguras donde guardarás tus credenciales. GitHub las cifra y nunca se muestran públicamente.

1. **Ve a tu repositorio en GitHub**
   - Abre tu navegador y ve a: `https://github.com/TU_USUARIO/Bot-NICEHASH`

2. **Accede a Settings**
   - Haz clic en la pestaña **Settings** (Configuración)

3. **Abre Secrets and variables**
   - En el menú lateral izquierdo, busca **Secrets and variables**
   - Haz clic en **Actions**

4. **Agregar los Secrets**
   - Haz clic en el botón verde **New repository secret**
   - Agrega cada uno de estos secrets:

   | Nombre del Secret | Valor | Dónde obtenerlo |
   |-------------------|-------|-----------------|
   | `NICEHASH_API_KEY` | Tu API Key de NiceHash | Tu archivo `.env` |
   | `NICEHASH_API_SECRET` | Tu API Secret de NiceHash | Tu archivo `.env` |
   | `NICEHASH_ORG_ID` | Tu Organization ID | Tu archivo `.env` |
   | `TELEGRAM_BOT_TOKEN` | Token de tu bot de Telegram | BotFather en Telegram |
   | `TELEGRAM_CHAT_ID` | Tu Chat ID de Telegram | userinfobot o getUpdates |

   **Importante**: Copia y pega exactamente los valores desde tu archivo `.env` (sin espacios ni comillas)

### Paso 3: Subir el Código a GitHub

Si aún no has subido tu código a GitHub:

```powershell
# Inicializar git (si no lo has hecho)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Configurar monitor de rigs con GitHub Actions"

# Conectar con tu repositorio de GitHub
git remote add origin https://github.com/TU_USUARIO/Bot-NICEHASH.git

# Subir el código
git push -u origin main
```

Si ya tienes el código en GitHub, solo actualiza:

```powershell
git add .
git commit -m "Actualizar configuración de GitHub Actions"
git push
```

### Paso 4: Verificar que Funciona

1. **Ve a la pestaña Actions** en tu repositorio de GitHub

2. **Verás el workflow** "Monitor Rigs NiceHash"

3. **Ejecutar manualmente** (primera vez):
   - Haz clic en el workflow "Monitor Rigs NiceHash"
   - Haz clic en "Run workflow" (botón en la derecha)
   - Selecciona la rama "main"
   - Haz clic en el botón verde "Run workflow"

4. **Espera unos segundos** y aparecerá una ejecución en progreso

5. **Verifica en Telegram** que recibiste una notificación

## 📊 Funcionamiento

### ⏱️ Frecuencia de Ejecución

El workflow se ejecuta:
- **Cada 5 minutos** automáticamente
- **Manualmente** cuando quieras desde GitHub

### 📱 Notificaciones que Recibirás

1. **Cuando un rig se cae**:
   ```
   🔴 Alerta: Rig Caído
   
   🖥️ Rig: 10x1x0x123
   📊 Estado: CAÍDO
   🕐 Hora: 2026-01-27 15:30:45
   
   ⚠️ El rig dejó de minar
   ```

2. **Cuando un rig se recupera**:
   ```
   ✅ Rig Recuperado
   
   🖥️ Rig: 10x1x0x123
   📊 Estado: ACTIVO
   🕐 Hora: 2026-01-27 15:35:12
   
   ✅ El rig ha vuelto a minar correctamente
   ```

### 💾 Persistencia de Estados

GitHub Actions guarda el archivo `rig_states.json` entre ejecuciones para recordar el estado anterior de los rigs y solo notificar cuando hay cambios.

## ⚙️ Personalización

### Cambiar la Frecuencia de Verificación

Edita el archivo [`.github/workflows/telegram-monitor.yml`](.github/workflows/telegram-monitor.yml):

```yaml
on:
  schedule:
    # Cambiar el cron aquí
    - cron: '*/5 * * * *'  # Cada 5 minutos
```

Ejemplos de cron:
- `*/1 * * * *` - Cada 1 minuto
- `*/10 * * * *` - Cada 10 minutos
- `*/30 * * * *` - Cada 30 minutos
- `0 * * * *` - Cada hora

**Nota**: Frecuencias muy altas pueden agotar tus minutos gratis de GitHub Actions.

### Limitar los Minutos Usados

Con 372 rigs, cada ejecución toma aproximadamente 30-60 segundos. 

Cálculo de uso mensual:
- **Cada 5 minutos**: ~8,640 ejecuciones/mes = ~7,200 minutos
- **Cada 10 minutos**: ~4,320 ejecuciones/mes = ~3,600 minutos
- **Cada 15 minutos**: ~2,880 ejecuciones/mes = ~2,400 minutos (Recomendado)

GitHub Actions ofrece **2,000 minutos gratis** al mes para cuentas gratuitas.

**Recomendación**: Usa `*/15 * * * *` (cada 15 minutos) para mantenerte dentro del límite gratuito.

## 🔧 Solución de Problemas

### El workflow no se ejecuta

1. **Verifica que los secrets estén configurados**:
   - Ve a Settings → Secrets and variables → Actions
   - Confirma que los 5 secrets estén creados

2. **Verifica que el archivo workflow esté en la ubicación correcta**:
   - Debe estar en: `.github/workflows/telegram-monitor.yml`

3. **Asegúrate de que el repositorio sea público** o tengas GitHub Actions habilitado en repos privados

### No recibo notificaciones en Telegram

1. **Verifica los secrets de Telegram**:
   - `TELEGRAM_BOT_TOKEN` debe ser correcto
   - `TELEGRAM_CHAT_ID` debe ser tu ID personal

2. **Inicia conversación con tu bot** en Telegram (envía `/start`)

3. **Revisa los logs del workflow**:
   - Ve a Actions → Selecciona una ejecución
   - Haz clic en "Verificar estado de rigs"
   - Revisa si hay errores

### Error: "API Key incorrecta"

Verifica que hayas copiado exactamente:
- `NICEHASH_API_KEY`
- `NICEHASH_API_SECRET`
- `NICEHASH_ORG_ID`

desde tu archivo `.env` (sin espacios ni comillas).

### Quiero detener las ejecuciones automáticas

1. Ve a tu repositorio en GitHub
2. Pestaña **Actions**
3. En el menú lateral, haz clic en "Monitor Rigs NiceHash"
4. Haz clic en los tres puntos (...)
5. Selecciona "Disable workflow"

## 📈 Monitoreo del Uso

Para ver cuántos minutos has usado:

1. Ve a tu perfil de GitHub
2. Settings → Billing and plans
3. Busca "Actions & Packages"
4. Verás el uso actual y el límite

## 🎯 Próximos Pasos

Una vez configurado, el sistema:
- ✅ Monitoreará tus 372 rigs automáticamente
- ✅ Te notificará en Telegram cuando haya cambios
- ✅ Funcionará 24/7 sin necesidad de tu PC

## 💡 Tips Adicionales

1. **Guarda tus secrets**: Anota tus tokens en un lugar seguro

2. **Monitorea tu uso**: Revisa regularmente cuántos minutos de Actions usas

3. **Ajusta la frecuencia**: Si te quedas sin minutos, aumenta el intervalo

4. **Combina con ejecución local**: Puedes usar GitHub Actions para alertas y ejecutar localmente para reportes detallados

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en la pestaña Actions de GitHub
2. Verifica que todos los secrets estén correctos
3. Asegúrate de que tu bot de Telegram esté activo
4. Consulta [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) para más ayuda con Telegram

---

¡Tu monitor de rigs ahora funciona en la nube! 🎉
