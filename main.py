"""
Script principal para obtener estadísticas de NiceHash
Muestra hashrate, mineros activos y producción mensual
"""
from datetime import datetime, timedelta
from nicehash_client import NiceHashClient
import json


def format_hashrate(hashrate: float, unit: str = 'H/s') -> str:
    """
    Formatea el hashrate a una unidad legible
    
    Args:
        hashrate: Valor del hashrate
        unit: Unidad del hashrate
        
    Returns:
        String formateado
    """
    if hashrate >= 1_000_000_000_000:
        return f"{hashrate/1_000_000_000_000:.2f} TH/s"
    elif hashrate >= 1_000_000_000:
        return f"{hashrate/1_000_000_000:.2f} GH/s"
    elif hashrate >= 1_000_000:
        return f"{hashrate/1_000_000:.2f} MH/s"
    elif hashrate >= 1_000:
        return f"{hashrate/1_000:.2f} KH/s"
    else:
        return f"{hashrate:.2f} H/s"


def print_separator(title: str = ""):
    """Imprime un separador visual"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    else:
        print("-" * 60)


def show_active_rigs(client: NiceHashClient):
    """Muestra información de rigs activos"""
    print_separator("INFORMACIÓN DE RIGS Y HASHRATE")
    
    try:
        rigs_data = client.get_rigs()
        
        if 'miningRigs' in rigs_data:
            rigs = rigs_data['miningRigs']
            total_rigs = len(rigs)
            active_rigs = sum(1 for rig in rigs if rig.get('minerStatus') == 'MINING')
            
            print(f"\n📊 Total de Rigs: {total_rigs}")
            print(f"✅ Rigs Activos: {active_rigs}")
            print(f"❌ Rigs Inactivos: {total_rigs - active_rigs}")
            
            print("\n" + "-" * 60)
            print("Detalle de Rigs:")
            print("-" * 60)
            
            for rig in rigs:
                name = rig.get('name', 'Sin nombre')
                status = rig.get('minerStatus', 'UNKNOWN')
                status_icon = "✅" if status == "MINING" else "❌"
                
                print(f"\n{status_icon} {name}")
                print(f"   Estado: {status}")
                
                # Mostrar hashrate por dispositivo
                if 'devices' in rig:
                    for device in rig['devices']:
                        device_name = device.get('name', 'Dispositivo')
                        speeds = device.get('speeds', [])
                        
                        if speeds:
                            for speed in speeds:
                                algo = speed.get('algorithm', 'N/A')
                                hashrate = float(speed.get('speed', 0))
                                print(f"   └─ {device_name} ({algo}): {format_hashrate(hashrate)}")
        else:
            print("⚠️  No se encontraron rigs")
            
    except Exception as e:
        print(f"❌ Error al obtener información de rigs: {e}")








def main():
    """Función principal"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "NICEHASH MINING STATISTICS" + " " * 22 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        # Inicializar cliente
        client = NiceHashClient()
        print("\n✓ Cliente inicializado correctamente")
        
        # Mostrar información
        show_active_rigs(client)
        
        print("\n" + "=" * 60)
        print("✓ Reporte completado exitosamente")
        print("=" * 60 + "\n")
        
    except ValueError as e:
        print(f"\n❌ Error de configuración: {e}")
        print("\n📝 Instrucciones:")
        print("1. Copia el archivo .env.example a .env")
        print("2. Edita el archivo .env con tus credenciales de NiceHash")
        print("3. Obtén tus credenciales en: https://www.nicehash.com/my/settings/keys")
        print()
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print()


if __name__ == "__main__":
    main()
