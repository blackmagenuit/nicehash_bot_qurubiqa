"""
Ejemplo de uso avanzado del cliente de NiceHash
Muestra cómo usar el cliente para crear scripts personalizados
"""
from nicehash_client import NiceHashClient
from datetime import datetime, timedelta


def calcular_rentabilidad_promedio(dias: int = 7):
    """
    Calcula la rentabilidad promedio de los últimos N días
    
    Args:
        dias: Número de días a analizar
    """
    client = NiceHashClient()
    
    to_date = datetime.now()
    from_date = to_date - timedelta(days=dias)
    
    earnings_data = client.get_daily_earnings(
        from_date.strftime('%Y-%m-%d'),
        to_date.strftime('%Y-%m-%d')
    )
    
    if 'data' in earnings_data:
        daily_earnings = earnings_data['data']
        
        if daily_earnings:
            total = sum(float(day.get('profitability', 0)) for day in daily_earnings)
            promedio = total / len(daily_earnings)
            
            print(f"\n📊 Análisis de rentabilidad ({dias} días)")
            print(f"   Total: {total:.8f} BTC")
            print(f"   Promedio diario: {promedio:.8f} BTC")
            print(f"   Proyección mensual (30 días): {promedio * 30:.8f} BTC")
            print(f"   Proyección anual (365 días): {promedio * 365:.8f} BTC")
            
            return promedio
    
    return 0


def alertar_si_rig_inactivo():
    """
    Verifica si hay rigs inactivos y muestra una alerta
    Útil para automatizar notificaciones
    """
    client = NiceHashClient()
    rigs_data = client.get_rigs()
    
    if 'miningRigs' in rigs_data:
        rigs_inactivos = [
            rig for rig in rigs_data['miningRigs'] 
            if rig.get('minerStatus') != 'MINING'
        ]
        
        if rigs_inactivos:
            print(f"\n⚠️  ALERTA: {len(rigs_inactivos)} rig(s) inactivo(s)!")
            for rig in rigs_inactivos:
                print(f"   • {rig.get('name', 'Sin nombre')}: {rig.get('minerStatus', 'UNKNOWN')}")
            return True
        else:
            print(f"\n✅ Todos los rigs están activos ({len(rigs_data['miningRigs'])} rigs)")
            return False
    
    return None


def comparar_algoritmos():
    """
    Compara el rendimiento de diferentes algoritmos
    """
    client = NiceHashClient()
    algo_stats = client.get_algo_stats()
    
    if 'algos' in algo_stats:
        print("\n📊 Comparación de algoritmos")
        print("-" * 70)
        print(f"{'Algoritmo':<25} {'Hashrate':<15} {'Balance no pagado':<15}")
        print("-" * 70)
        
        for algo in algo_stats['algos']:
            algo_name = algo.get('a', 'N/A')
            speed = float(algo.get('sa', 0))
            unpaid = float(algo.get('up', 0))
            
            # Formatear hashrate
            if speed >= 1_000_000_000:
                speed_str = f"{speed/1_000_000_000:.2f} GH/s"
            elif speed >= 1_000_000:
                speed_str = f"{speed/1_000_000:.2f} MH/s"
            elif speed >= 1_000:
                speed_str = f"{speed/1_000:.2f} KH/s"
            else:
                speed_str = f"{speed:.2f} H/s"
            
            print(f"{algo_name:<25} {speed_str:<15} {unpaid:.8f} BTC")


def obtener_mejor_dia():
    """
    Encuentra el día con mayor producción en el último mes
    """
    client = NiceHashClient()
    
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    
    earnings_data = client.get_daily_earnings(
        from_date.strftime('%Y-%m-%d'),
        to_date.strftime('%Y-%m-%d')
    )
    
    if 'data' in earnings_data:
        daily_earnings = earnings_data['data']
        
        if daily_earnings:
            mejor_dia = max(daily_earnings, key=lambda x: float(x.get('profitability', 0)))
            peor_dia = min(daily_earnings, key=lambda x: float(x.get('profitability', 0)))
            
            print(f"\n🏆 Mejor día del mes:")
            print(f"   Fecha: {mejor_dia.get('date', 'N/A')}")
            print(f"   Producción: {float(mejor_dia.get('profitability', 0)):.8f} BTC")
            
            print(f"\n📉 Día con menor producción:")
            print(f"   Fecha: {peor_dia.get('date', 'N/A')}")
            print(f"   Producción: {float(peor_dia.get('profitability', 0)):.8f} BTC")
            
            diferencia = float(mejor_dia.get('profitability', 0)) - float(peor_dia.get('profitability', 0))
            porcentaje = (diferencia / float(peor_dia.get('profitability', 0.001)) * 100)
            
            print(f"\n📊 Variación: {diferencia:.8f} BTC ({porcentaje:.1f}%)")


def monitorear_hashrate():
    """
    Monitorea el hashrate actual y lo compara con el esperado
    """
    client = NiceHashClient()
    algo_stats = client.get_algo_stats()
    
    print("\n⚡ Monitoreo de Hashrate")
    print("-" * 60)
    
    if 'algos' in algo_stats:
        total_devices = 0
        
        for algo in algo_stats['algos']:
            algo_name = algo.get('a', 'N/A')
            speed_accepted = float(algo.get('sa', 0))
            speed_rejected = float(algo.get('sr', 0))
            
            if speed_accepted > 0:
                rejection_rate = (speed_rejected / (speed_accepted + speed_rejected)) * 100
                
                print(f"\n{algo_name}:")
                
                # Formatear velocidad
                if speed_accepted >= 1_000_000_000:
                    speed_str = f"{speed_accepted/1_000_000_000:.2f} GH/s"
                elif speed_accepted >= 1_000_000:
                    speed_str = f"{speed_accepted/1_000_000:.2f} MH/s"
                else:
                    speed_str = f"{speed_accepted/1_000:.2f} KH/s"
                
                print(f"  ✓ Hashrate: {speed_str}")
                print(f"  ✓ Tasa de rechazo: {rejection_rate:.2f}%")
                
                # Alertas
                if rejection_rate > 5:
                    print(f"  ⚠️  ALERTA: Tasa de rechazo alta!")
                elif rejection_rate > 2:
                    print(f"  ⚠️  Advertencia: Tasa de rechazo moderada")
                else:
                    print(f"  ✅ Tasa de rechazo normal")


def main():
    """Ejecuta todos los ejemplos"""
    print("\n╔" + "═" * 58 + "╗")
    print("║" + " " * 8 + "NICEHASH - USO AVANZADO" + " " * 27 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        # Verificar rigs inactivos
        alertar_si_rig_inactivo()
        
        # Calcular rentabilidad promedio
        calcular_rentabilidad_promedio(7)
        calcular_rentabilidad_promedio(30)
        
        # Comparar algoritmos
        comparar_algoritmos()
        
        # Encontrar mejor día
        obtener_mejor_dia()
        
        # Monitorear hashrate
        monitorear_hashrate()
        
        print("\n" + "=" * 60)
        print("✓ Análisis completado")
        print("=" * 60 + "\n")
        
    except ValueError as e:
        print(f"\n❌ Error de configuración: {e}")
        print("Asegúrate de haber configurado el archivo .env correctamente\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
