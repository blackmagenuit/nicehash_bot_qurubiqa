# Script para automatizar la exportación diaria de estadísticas
# Guarda los reportes en una carpeta "reportes" con la fecha
#
# Para programar con el Programador de Tareas de Windows:
# 1. Abre el Programador de tareas (taskschd.msc)
# 2. Crear tarea básica
# 3. Nombre: "NiceHash Stats Diario"
# 4. Desencadenador: Diariamente a las 00:00
# 5. Acción: Iniciar un programa
#    - Programa: powershell.exe
#    - Argumentos: -ExecutionPolicy Bypass -File "C:\ruta\completa\exportar_diario.ps1"
#    - Iniciar en: C:\ruta\completa\Nicehash

# Obtener fecha actual
$fecha = Get-Date -Format "yyyy-MM-dd"
$hora = Get-Date -Format "HH-mm-ss"

# Crear carpeta de reportes si no existe
$carpetaReportes = "reportes"
if (-not (Test-Path $carpetaReportes)) {
    New-Item -ItemType Directory -Path $carpetaReportes | Out-Null
    Write-Host "✓ Carpeta 'reportes' creada" -ForegroundColor Green
}

# Nombre del archivo
$nombreArchivo = "$carpetaReportes\nicehash_stats_$fecha`_$hora.json"

# Ejecutar exportación
Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  EXPORTACION AUTOMATICA - NICEHASH STATS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📅 Fecha: $fecha $hora" -ForegroundColor Yellow
Write-Host "📁 Archivo: $nombreArchivo" -ForegroundColor Yellow
Write-Host ""

try {
    # Ejecutar script de exportación
    python export_stats.py $nombreArchivo
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Exportación completada exitosamente" -ForegroundColor Green
        
        # Opcional: Limpiar reportes antiguos (más de 30 días)
        $diasAMantener = 30
        $fechaLimite = (Get-Date).AddDays(-$diasAMantener)
        
        Write-Host ""
        Write-Host "🧹 Limpiando reportes antiguos (>$diasAMantener días)..." -ForegroundColor Yellow
        
        $archivosAntiguos = Get-ChildItem $carpetaReportes -Filter "nicehash_stats_*.json" | 
            Where-Object { $_.LastWriteTime -lt $fechaLimite }
        
        if ($archivosAntiguos.Count -gt 0) {
            foreach ($archivo in $archivosAntiguos) {
                Remove-Item $archivo.FullName
                Write-Host "   • Eliminado: $($archivo.Name)" -ForegroundColor Gray
            }
            Write-Host "✓ $($archivosAntiguos.Count) archivo(s) antiguo(s) eliminado(s)" -ForegroundColor Green
        } else {
            Write-Host "✓ No hay archivos antiguos para eliminar" -ForegroundColor Green
        }
        
        # Mostrar estadísticas de almacenamiento
        $totalArchivos = (Get-ChildItem $carpetaReportes -Filter "nicehash_stats_*.json").Count
        $tamañoTotal = (Get-ChildItem $carpetaReportes -Filter "nicehash_stats_*.json" | 
            Measure-Object -Property Length -Sum).Sum / 1MB
        
        Write-Host ""
        Write-Host "📊 Estadísticas de reportes:" -ForegroundColor Cyan
        Write-Host "   Total de reportes: $totalArchivos" -ForegroundColor White
        Write-Host "   Espacio utilizado: $([math]::Round($tamañoTotal, 2)) MB" -ForegroundColor White
        
    } else {
        Write-Host ""
        Write-Host "❌ Error en la exportación" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Error al ejecutar el script: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Log de ejecución (opcional)
$logFile = "reportes\exportacion.log"
$logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Exportación completada: $nombreArchivo"
Add-Content -Path $logFile -Value $logEntry

exit 0
