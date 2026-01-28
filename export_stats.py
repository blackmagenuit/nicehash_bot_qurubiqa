"""
Script para exportar estadísticas de NiceHash a formato JSON
Útil para integraciones con otros sistemas o análisis de datos
"""
import json
from datetime import datetime, timedelta
from nicehash_client import NiceHashClient


def export_statistics(output_file: str = "nicehash_stats.json"):
    """
    Exporta todas las estadísticas a un archivo JSON
    
    Args:
        output_file: Nombre del archivo de salida
    """
    try:
        print(f"🔄 Obteniendo datos de NiceHash...")
        client = NiceHashClient()
        
        # Obtener todas las estadísticas
        data = {
            "timestamp": datetime.now().isoformat(),
            "rigs": {}
        }
        
        # Rigs
        try:
            print("  └─ Obteniendo información de rigs...")
            data["rigs"] = client.get_rigs()
        except Exception as e:
            print(f"  └─ ⚠️  Error al obtener rigs: {e}")
            data["rigs"] = {"error": str(e)}
        
        # Guardar a archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Datos exportados exitosamente a: {output_file}")
        print(f"📊 Tamaño del archivo: {len(json.dumps(data))} bytes")
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("RESUMEN DE LA EXPORTACIÓN")
        print("="*60)
        
        if 'miningRigs' in data['rigs']:
            print(f"✓ Rigs exportados: {len(data['rigs']['miningRigs'])}")
        
        print("="*60)
        
        return data
        
    except ValueError as e:
        print(f"\n❌ Error de configuración: {e}")
        print("\n📝 Instrucciones:")
        print("1. Copia el archivo .env.example a .env")
        print("2. Edita el archivo .env con tus credenciales de NiceHash")
        print("3. Obtén tus credenciales en: https://www.nicehash.com/my/settings/keys")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return None


def generate_summary_report(json_file: str = "nicehash_stats.json"):
    """
    Genera un reporte resumido a partir del archivo JSON exportado
    
    Args:
        json_file: Archivo JSON con las estadísticas
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n" + "="*60)
        print("REPORTE RESUMIDO")
        print("="*60)
        
        timestamp = data.get('timestamp', 'N/A')
        print(f"\n📅 Fecha del reporte: {timestamp}")
        
        # Resumen de rigs
        if 'miningRigs' in data.get('rigs', {}):
            rigs = data['rigs']['miningRigs']
            active = sum(1 for r in rigs if r.get('minerStatus') == 'MINING')
            print(f"\n🖥️  Rigs: {len(rigs)} total, {active} activos")
        
        print("\n" + "="*60)
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {json_file}")
        print("💡 Primero ejecuta la exportación con: python export_stats.py")
    except Exception as e:
        print(f"❌ Error al leer el reporte: {e}")


if __name__ == "__main__":
    import sys
    
    print("\n╔" + "═" * 58 + "╗")
    print("║" + " " * 8 + "NICEHASH STATS EXPORT TOOL" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝\n")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "summary":
            # Generar resumen desde archivo existente
            json_file = sys.argv[2] if len(sys.argv) > 2 else "nicehash_stats.json"
            generate_summary_report(json_file)
        else:
            # Exportar con nombre personalizado
            export_statistics(sys.argv[1])
    else:
        # Exportar con nombre por defecto
        data = export_statistics()
        
        if data:
            print("\n💡 Para ver un resumen ejecuta:")
            print("   python export_stats.py summary")
            print("\n💡 Para exportar con otro nombre:")
            print("   python export_stats.py mi_reporte.json")
