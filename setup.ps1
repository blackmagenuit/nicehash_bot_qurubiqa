# Script de instalación y configuración para NiceHash Stats
# Ejecutar con: .\setup.ps1

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          NICEHASH STATS - INSTALACION                    ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "🔍 Verificando instalación de Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "   Descarga Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Instalar dependencias
Write-Host ""
Write-Host "📦 Instalando dependencias de Python..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

# Verificar archivo .env
Write-Host ""
Write-Host "⚙️  Verificando configuración..." -ForegroundColor Yellow

if (Test-Path .env) {
    Write-Host "✓ Archivo .env encontrado" -ForegroundColor Green
    
    # Leer el archivo .env y verificar si está configurado
    $envContent = Get-Content .env -Raw
    if ($envContent -match "NICEHASH_API_KEY=\s*$" -or $envContent -notmatch "NICEHASH_API_KEY=") {
        Write-Host ""
        Write-Host "⚠️  El archivo .env existe pero no está configurado" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📝 Para configurar tus credenciales:" -ForegroundColor Cyan
        Write-Host "   1. Ve a: https://www.nicehash.com/my/settings/keys" -ForegroundColor White
        Write-Host "   2. Crea una nueva API Key con permiso VMDS" -ForegroundColor White
        Write-Host "   3. Edita el archivo .env con tus credenciales" -ForegroundColor White
        Write-Host ""
        
        $respuesta = Read-Host "¿Quieres abrir el archivo .env ahora para editarlo? (S/N)"
        if ($respuesta -eq "S" -or $respuesta -eq "s") {
            notepad .env
        }
    } else {
        Write-Host "✓ Archivo .env está configurado" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  Archivo .env no encontrado, usando .env.example como base" -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✓ Archivo .env creado" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Ahora debes editar el archivo .env con tus credenciales" -ForegroundColor Cyan
    Write-Host "   1. Ve a: https://www.nicehash.com/my/settings/keys" -ForegroundColor White
    Write-Host "   2. Crea una nueva API Key con permiso VMDS" -ForegroundColor White
    Write-Host "   3. Edita el archivo .env con tus credenciales" -ForegroundColor White
    Write-Host ""
    
    $respuesta = Read-Host "¿Quieres abrir el archivo .env ahora para editarlo? (S/N)"
    if ($respuesta -eq "S" -or $respuesta -eq "s") {
        notepad .env
    }
}

Write-Host ""
Write-Host "══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host "══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Preguntar si quiere ejecutar el test
Write-Host "¿Quieres probar la configuración ahora? (S/N): " -NoNewline -ForegroundColor Yellow
$respuesta = Read-Host

if ($respuesta -eq "S" -or $respuesta -eq "s") {
    Write-Host ""
    python test_config.py
} else {
    Write-Host ""
    Write-Host "🚀 Para ejecutar el programa:" -ForegroundColor Yellow
    Write-Host "   python main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "🧪 Para probar tu configuración:" -ForegroundColor Yellow
    Write-Host "   python test_config.py" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Para exportar estadísticas a JSON:" -ForegroundColor Yellow
    Write-Host "   python export_stats.py" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 Lee el archivo README.md para más información" -ForegroundColor Yellow
    Write-Host ""
}
