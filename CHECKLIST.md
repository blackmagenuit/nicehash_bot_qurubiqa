# ✅ Checklist: Configuración de Telegram + GitHub Actions

## 📋 Estado Actual

✅ **Completado:**
- ✅ API de NiceHash configurada
- ✅ Sistema obtiene 372 rigs correctamente (con paginación)
- ✅ Scripts principales funcionando
- ✅ Workflow de GitHub Actions creado (`.github/workflows/telegram-monitor.yml`)
- ✅ Documentación completa creada

## 🎯 Lo que te falta hacer

### 1️⃣ Configurar Telegram (15 minutos)

#### Paso 1.1: Crear Bot de Telegram
- [ ] Abre Telegram y busca: **@BotFather**
- [ ] Envía el comando: `/newbot`
- [ ] Elige un nombre (ej: "NiceHash Monitor")
- [ ] Elige un username terminado en "bot" (ej: "minicehash_bot")
- [ ] **Copia y guarda el token** (se ve así: `1234567890:ABCdefGHI...`)

#### Paso 1.2: Obtener tu Chat ID
- [ ] Busca tu bot en Telegram (el username que elegiste)
- [ ] Haz clic en **Start** o envía `/start`
- [ ] Busca en Telegram: **@userinfobot**
- [ ] Envíale `/start`
- [ ] **Copia tu Chat ID** (número que te responda)

#### Paso 1.3: Agregar a .env
- [ ] Abre el archivo `.env` en tu editor
- [ ] Agrega estas dos líneas al final:
  ```env
  TELEGRAM_BOT_TOKEN=tu_token_aqui
  TELEGRAM_CHAT_ID=tu_chat_id_aqui
  ```
- [ ] Guarda el archivo

#### Paso 1.4: Probar configuración
- [ ] Ejecuta en PowerShell:
  ```powershell
  python test_telegram.py
  ```
- [ ] Verifica que recibes un mensaje en Telegram

### 2️⃣ Probar el Monitor Localmente (5 minutos)

- [ ] Ejecuta el monitor una vez:
  ```powershell
  python telegram_bot.py --check-once
  ```
- [ ] Verifica que funciona sin errores

### 3️⃣ Configurar GitHub Actions (20 minutos)

#### Paso 3.1: Preparar el repositorio
- [ ] Asegúrate de tener una cuenta en GitHub
- [ ] Si no tienes el repo creado:
  - Ve a https://github.com/new
  - Crea un repositorio (puede ser privado)
  - Copia la URL del repositorio

#### Paso 3.2: Subir código a GitHub
- [ ] Abre PowerShell en la carpeta del proyecto
- [ ] Ejecuta estos comandos:
  ```powershell
  # Si es la primera vez
  git init
  git add .
  git commit -m "Configurar monitor con Telegram y GitHub Actions"
  git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
  git push -u origin main
  
  # Si ya existe el repo, solo actualiza
  git add .
  git commit -m "Actualizar configuración"
  git push
  ```

#### Paso 3.3: Configurar Secrets en GitHub
- [ ] Ve a tu repositorio en GitHub
- [ ] Haz clic en **Settings** (pestaña superior)
- [ ] En el menú lateral: **Secrets and variables** → **Actions**
- [ ] Haz clic en **New repository secret**
- [ ] Agrega estos 5 secrets uno por uno:

| Nombre | Valor | Dónde lo encuentro |
|--------|-------|-------------------|
| `NICEHASH_API_KEY` | Tu API Key | Archivo `.env` → línea `NICEHASH_API_KEY=...` |
| `NICEHASH_API_SECRET` | Tu API Secret | Archivo `.env` → línea `NICEHASH_API_SECRET=...` |
| `NICEHASH_ORG_ID` | Tu Organization ID | Archivo `.env` → línea `NICEHASH_ORG_ID=...` |
| `TELEGRAM_BOT_TOKEN` | Token de tu bot | Archivo `.env` → línea `TELEGRAM_BOT_TOKEN=...` |
| `TELEGRAM_CHAT_ID` | Tu Chat ID | Archivo `.env` → línea `TELEGRAM_CHAT_ID=...` |

**Importante:** Copia los valores exactos desde tu `.env`, sin las comillas ni espacios.

#### Paso 3.4: Activar el Workflow
- [ ] Ve a la pestaña **Actions** en tu repositorio
- [ ] Si aparece un mensaje para habilitar workflows, haz clic en **Enable**
- [ ] Busca el workflow "Monitor Rigs NiceHash"
- [ ] Haz clic en el workflow
- [ ] Haz clic en **Run workflow** (botón derecha)
- [ ] Selecciona la rama `main`
- [ ] Haz clic en **Run workflow** (botón verde)

#### Paso 3.5: Verificar que funciona
- [ ] Espera 30-60 segundos
- [ ] Verifica en Telegram que NO recibiste notificaciones (es normal en la primera ejecución)
- [ ] En GitHub, haz clic en la ejecución que aparece
- [ ] Revisa que todos los pasos tengan ✅ verde
- [ ] Si hay errores, revisa que los secrets estén correctos

### 4️⃣ Ajustar frecuencia (opcional)

Si quieres cambiar cada cuánto se ejecuta:

- [ ] Edita el archivo: `.github/workflows/telegram-monitor.yml`
- [ ] Cambia la línea: `- cron: '*/5 * * * *'`
  - `*/5` = cada 5 minutos
  - `*/10` = cada 10 minutos
  - `*/15` = cada 15 minutos (recomendado para no gastar minutos)
- [ ] Guarda y haz push:
  ```powershell
  git add .
  git commit -m "Ajustar frecuencia"
  git push
  ```

## 🎉 ¡Listo!

Una vez completado, tendrás:
- ✅ Monitor automático en la nube (GitHub Actions)
- ✅ Notificaciones en Telegram cuando un rig se cae o recupera
- ✅ Verificación automática cada 5 minutos (o la frecuencia que elijas)
- ✅ Funciona 24/7 sin necesidad de tener tu PC encendida

## 📚 Guías Detalladas

Si necesitas más ayuda:
- **[TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)** - Guía detallada de Telegram
- **[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)** - Guía completa de GitHub Actions

## 🆘 Problemas Comunes

### No recibo notificaciones en Telegram
1. Verifica que hayas hecho Start con tu bot en Telegram
2. Revisa que el `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` estén correctos en los secrets
3. Ejecuta `python test_telegram.py` localmente para verificar

### Error en GitHub Actions
1. Ve a Actions → Selecciona la ejecución con error → Revisa los logs
2. Verifica que los 5 secrets estén configurados correctamente
3. Asegúrate de copiar los valores exactos desde tu `.env`

### "No se encontró archivo de estados previos"
- Es normal en la primera ejecución
- El archivo `rig_states.json` se creará automáticamente
- En la primera ejecución no habrá notificaciones

---

💡 **Tip:** Ejecuta primero el monitor localmente con `python telegram_bot.py` para que cree el archivo de estados inicial, luego súbelo a GitHub.
