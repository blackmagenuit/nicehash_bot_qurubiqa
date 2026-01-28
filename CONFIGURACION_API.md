# 🔑 Guía Detallada: Configuración de API de NiceHash

Esta guía te ayudará paso a paso a obtener y configurar tus credenciales de API de NiceHash.

## 📋 Índice

1. [Crear una cuenta en NiceHash](#1-crear-una-cuenta-en-nicehash)
2. [Generar una API Key](#2-generar-una-api-key)
3. [Configurar las credenciales](#3-configurar-las-credenciales)
4. [Verificar la configuración](#4-verificar-la-configuración)
5. [Solución de problemas](#5-solución-de-problemas)

---

## 1. Crear una cuenta en NiceHash

Si aún no tienes una cuenta:

1. Ve a [https://www.nicehash.com](https://www.nicehash.com)
2. Haz clic en "Sign Up" (Registrarse)
3. Completa el formulario de registro
4. Verifica tu correo electrónico
5. Activa la autenticación de dos factores (2FA) - **IMPORTANTE para la seguridad**

---

## 2. Generar una API Key

### Paso 1: Acceder a la configuración de API Keys

1. Inicia sesión en [https://www.nicehash.com](https://www.nicehash.com)
2. Haz clic en tu nombre de usuario (esquina superior derecha)
3. Selecciona **"Settings"** (Configuración)
4. En el menú lateral, haz clic en **"API Keys"**

### Paso 2: Crear una nueva API Key

1. Verás tu **Organization ID** justo arriba del botón "+ Create new API key"
   - **IMPORTANTE**: Copia este ID, lo necesitarás después
   
2. Haz clic en **"+ Create new API key"**

3. Se abrirá un formulario. Complétalo:

   **API Key Name (Nombre)**
   ```
   Mining Stats Monitor
   ```
   *(Puedes usar el nombre que prefieras)*

   **Permissions (Permisos)**
   
   Selecciona **SOLO** estos permisos:
   - ✅ **VMDS** - View mining data and statistics
   
   ⚠️ **IMPORTANTE**: NO selecciones permisos de retiro (WIFU) ni de gestión de fondos
   
   **IP Whitelist** (Opcional pero recomendado)
   - Si siempre ejecutas el script desde la misma IP, agrégala aquí
   - Puedes encontrar tu IP en: [https://whatismyipaddress.com](https://whatismyipaddress.com)

4. Haz clic en **"Generate API Key"**

### Paso 3: Guardar las credenciales

**🚨 ATENCIÓN: Esta es la ÚNICA vez que verás el API Secret**

Después de crear la API Key, verás una ventana con:

```
API Key: 4ebd366d-76f4-4400-a3b6-e51515d054d6
API Secret: fd8a1652-728b-42fe-82b8-f623e56da887...
Organization ID: da41b3bc-3d0b-4226-b7ea-aee73f94a518
```

1. **Copia el API Key** (primer campo)
2. **Copia el API Secret** (segundo campo - cadena larga)
3. **Copia el Organization ID** (lo viste antes de crear la key)

⚠️ **NO cierres esta ventana hasta que hayas copiado toda la información**

⚠️ **NUNCA compartas estas credenciales con nadie**

---

## 3. Configurar las credenciales

### Opción 1: Editar manualmente el archivo .env

1. Abre el archivo `.env` en un editor de texto (Notepad, VSCode, etc.)

2. Pega tus credenciales:

```env
NICEHASH_API_KEY=4ebd366d-76f4-4400-a3b6-e51515d054d6
NICEHASH_API_SECRET=fd8a1652-728b-42fe-82b8-f623e56da887-0750f5bf-ce66-4ca7-8b84-93651abc723b
NICEHASH_ORG_ID=da41b3bc-3d0b-4226-b7ea-aee73f94a518
NICEHASH_API_URL=https://api2.nicehash.com
```

3. Guarda el archivo

### Opción 2: Usar el script de configuración

```powershell
.\setup.ps1
```

El script te guiará en el proceso.

---

## 4. Verificar la configuración

Para verificar que todo está correctamente configurado:

```powershell
python main.py
```

Si ves algo como esto, ¡todo está correcto!:

```
╔══════════════════════════════════════════════════════════╗
║          NICEHASH MINING STATISTICS                      ║
╚══════════════════════════════════════════════════════════╝

✓ Cliente inicializado correctamente

============================================================
  INFORMACIÓN DE RIGS Y HASHRATE
============================================================
...
```

---

## 5. Solución de problemas

### Error: "NICEHASH_API_KEY no está configurada"

**Causa**: El archivo `.env` no existe o está vacío

**Solución**:
1. Verifica que el archivo `.env` existe en la carpeta del proyecto
2. Abre el archivo y verifica que las credenciales estén presentes
3. Asegúrate de que no hay espacios extra antes o después del `=`

Correcto:
```env
NICEHASH_API_KEY=4ebd366d-76f4-4400-a3b6-e51515d054d6
```

Incorrecto:
```env
NICEHASH_API_KEY = 4ebd366d-76f4-4400-a3b6-e51515d054d6
NICEHASH_API_KEY=
```

### Error 401: "Unauthorized"

**Causa**: Las credenciales son incorrectas o la API Key no tiene los permisos necesarios

**Solución**:
1. Verifica que copiaste correctamente:
   - El API Key completo
   - El API Secret completo (es una cadena larga)
   - El Organization ID correcto

2. Verifica que la API Key tenga el permiso **VMDS** activado:
   - Ve a [https://www.nicehash.com/my/settings/keys](https://www.nicehash.com/my/settings/keys)
   - Busca tu API Key
   - Verifica que tenga el permiso "View mining data and statistics"

3. Si todo lo anterior está correcto, crea una nueva API Key:
   - Elimina la API Key antigua
   - Crea una nueva siguiendo los pasos de la sección 2
   - Actualiza el archivo `.env` con las nuevas credenciales

### Error 429: "Too Many Requests"

**Causa**: Has hecho demasiadas peticiones en poco tiempo

**Solución**:
- Espera 5-10 minutos antes de volver a ejecutar el script
- NiceHash tiene límites de rate limiting en su API

### Error: "ModuleNotFoundError: No module named 'requests'"

**Causa**: Las dependencias no están instaladas

**Solución**:
```powershell
pip install -r requirements.txt
```

### La API Key no aparece o fue eliminada

**Problema**: Cerraste la ventana sin copiar el API Secret

**Solución**:
- No es posible recuperar el API Secret
- Debes crear una nueva API Key
- Puedes eliminar la API Key antigua desde la configuración

### Error: "X-Time header is out of sync"

**Causa**: El reloj de tu computadora no está sincronizado

**Solución**:
1. En Windows, abre Configuración > Hora e idioma
2. Activa "Establecer la hora automáticamente"
3. Si ya está activado, desactívalo y vuelve a activarlo
4. Verifica que la zona horaria sea correcta

---

## 🔒 Mejores Prácticas de Seguridad

1. **Permisos mínimos**: Solo otorga los permisos necesarios (VMDS para este proyecto)

2. **IP Whitelist**: Si es posible, configura el whitelist de IPs

3. **Rotación de keys**: Cambia tu API Key cada 3-6 meses

4. **No compartas**: Nunca compartas tu archivo `.env` o tus credenciales

5. **Backup seguro**: Si necesitas guardar un backup, encríptalo

6. **Git**: Asegúrate de que `.env` está en tu `.gitignore`

7. **2FA**: Siempre mantén activada la autenticación de dos factores en NiceHash

---

## 📞 ¿Necesitas más ayuda?

- **Documentación oficial**: [https://www.nicehash.com/docs/](https://www.nicehash.com/docs/)
- **Soporte de NiceHash**: [https://www.nicehash.com/support](https://www.nicehash.com/support)
- **README principal**: [README.md](README.md)

---

## ✅ Checklist de configuración

Usa esta lista para verificar que todo está correcto:

- [ ] Cuenta de NiceHash creada y verificada
- [ ] 2FA activado en la cuenta
- [ ] API Key creada con permiso VMDS
- [ ] API Key copiado correctamente
- [ ] API Secret copiado correctamente (cadena larga)
- [ ] Organization ID copiado correctamente
- [ ] Archivo `.env` creado
- [ ] Credenciales pegadas en `.env` sin espacios extra
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Script de prueba ejecutado correctamente (`python main.py`)

Si todos los items están marcados, ¡estás listo para usar el sistema! 🎉
