"""
Bot de Telegram para monitorear rigs de NiceHash
Envía notificaciones cuando los rigs cambian de estado (activo/caído)
"""
import time
import json
import requests
from datetime import datetime, timedelta, timezone
from nicehash_client import NiceHashClient
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ACCOUNT_NAME

# Zona horaria de Paraguay (GMT-3)
PARAGUAY_TZ = timezone(timedelta(hours=-3))

def get_paraguay_time():
    """Retorna la hora actual en zona horaria de Paraguay"""
    return datetime.now(PARAGUAY_TZ)


class TelegramNotifier:
    """Clase para enviar notificaciones a Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Inicializa el notificador de Telegram
        
        Args:
            bot_token: Token del bot de Telegram
            chat_id: ID del chat donde enviar mensajes
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message: str) -> bool:
        """
        Envía un mensaje a Telegram
        
        Args:
            message: Texto del mensaje
            
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Error al enviar mensaje a Telegram: {e}")
            return False


class RigMonitor:
    """Clase para monitorear el estado de los rigs"""
    
    def __init__(self, notifier: TelegramNotifier):
        """
        Inicializa el monitor de rigs
        
        Args:
            notifier: Instancia de TelegramNotifier
        """
        self.client = NiceHashClient()
        self.notifier = notifier
        self.previous_states = {}
        self.state_file = "rig_states.json"
        self.stats_file = "daily_stats.json"
        self.load_states()
    
    def load_states(self):
        """Carga los estados previos desde archivo"""
        try:
            with open(self.state_file, 'r') as f:
                self.previous_states = json.load(f)
            print(f"✓ Estados previos cargados: {len(self.previous_states)} rigs")
        except FileNotFoundError:
            print("ℹ️  No se encontró archivo de estados previos, comenzando desde cero")
            self.previous_states = {}
        except Exception as e:
            print(f"⚠️  Error al cargar estados: {e}")
            self.previous_states = {}
    
    def save_states(self):
        """Guarda los estados actuales a archivo"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.previous_states, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error al guardar estados: {e}")
    
    def save_hourly_stats(self, total, active, offline):
        """Guarda estadísticas horarias para el reporte diario"""
        try:
            current_date = get_paraguay_time().strftime('%Y-%m-%d')
            current_hour = get_paraguay_time().strftime('%Y-%m-%d %H:%M')
            
            # Cargar estadísticas existentes
            stats = {}
            try:
                with open(self.stats_file, 'r') as f:
                    stats = json.load(f)
            except FileNotFoundError:
                pass
            
            # Inicializar día si no existe
            if current_date not in stats:
                stats[current_date] = []
            
            # Agregar datos de esta hora
            stats[current_date].append({
                'timestamp': current_hour,
                'total': total,
                'active': active,
                'offline': offline
            })
            
            # Guardar
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
            
        except Exception as e:
            print(f"⚠️  Error al guardar estadísticas: {e}")
    
    def send_daily_report(self):
        """Envía el reporte diario con promedios del día anterior"""
        try:
            yesterday = (get_paraguay_time() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Cargar estadísticas
            try:
                with open(self.stats_file, 'r') as f:
                    stats = json.load(f)
            except FileNotFoundError:
                print("⚠️  No hay estadísticas para generar reporte diario")
                return
            
            if yesterday not in stats:
                print(f"⚠️  No hay datos para {yesterday}")
                return
            
            day_stats = stats[yesterday]
            
            if not day_stats:
                print(f"⚠️  No hay datos para {yesterday}")
                return
            
            # Calcular promedios
            total_checks = len(day_stats)
            avg_total = sum(s['total'] for s in day_stats) / total_checks
            avg_active = sum(s['active'] for s in day_stats) / total_checks
            avg_offline = sum(s['offline'] for s in day_stats) / total_checks
            
            # Calcular máximos y mínimos
            max_active = max(s['active'] for s in day_stats)
            min_active = min(s['active'] for s in day_stats)
            max_offline = max(s['offline'] for s in day_stats)
            min_offline = min(s['offline'] for s in day_stats)
            
            # Preparar mensaje
            message = f"📊 <b>Resumen Diario - {ACCOUNT_NAME}</b>\n\n"
            message += f"📅 <b>Fecha:</b> {yesterday}\n"
            message += f"🕐 <b>Generado:</b> {get_paraguay_time().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            message += f"📈 <b>Promedios del Día:</b>\n"
            message += f"• Total de Rigs: {avg_total:.0f}\n"
            message += f"• Activos: {avg_active:.0f} (promedio)\n"
            message += f"• Offline: {avg_offline:.0f} (promedio)\n\n"
            message += f"📊 <b>Rangos:</b>\n"
            message += f"• Activos: {min_active} - {max_active}\n"
            message += f"• Offline: {min_offline} - {max_offline}\n\n"
            message += f"📋 <b>Lecturas:</b> {total_checks} checks durante el día"
            
            self.notifier.send_message(message)
            print("✓ Reporte diario enviado")
            
            # Limpiar datos antiguos (mantener solo últimos 7 días)
            cutoff_date = (get_paraguay_time() - timedelta(days=7)).strftime('%Y-%m-%d')
            stats = {k: v for k, v in stats.items() if k >= cutoff_date}
            
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
            
        except Exception as e:
            print(f"❌ Error al enviar reporte diario: {e}")
    
    def check_rigs(self):
        """Verifica el estado de todos los rigs y envía notificaciones si hay cambios"""
        try:
            print(f"\n[{get_paraguay_time().strftime('%Y-%m-%d %H:%M:%S')}] Verificando rigs...")
            
            rigs_data = self.client.get_rigs()
            
            if 'miningRigs' not in rigs_data:
                print("⚠️  No se encontraron rigs")
                return
            
            rigs = rigs_data['miningRigs']
            current_time = get_paraguay_time().strftime('%Y-%m-%d %H:%M:%S')
            
            # Contadores
            active_count = 0
            offline_count = 0
            
            # Listas para rigs que cambiaron
            rigs_caidos = []
            rigs_recuperados = []
            
            for rig in rigs:
                rig_name = rig.get('name', 'Sin nombre')
                rig_status = rig.get('minerStatus', 'UNKNOWN')
                
                # Contar estados
                if rig_status == 'MINING':
                    active_count += 1
                else:
                    offline_count += 1
                
                # Verificar cambios de estado
                previous_status = self.previous_states.get(rig_name)
                
                if previous_status is None:
                    # Primera vez que vemos este rig
                    self.previous_states[rig_name] = rig_status
                    print(f"  📋 {rig_name}: {rig_status} (nuevo)")
                    
                elif previous_status != rig_status:
                    # El estado cambió
                    self.previous_states[rig_name] = rig_status
                    
                    if rig_status == 'MINING':
                        # Rig volvió a estar activo
                        rigs_recuperados.append(rig_name)
                        print(f"  ✅ {rig_name}: {previous_status} → {rig_status}")
                    else:
                        # Rig se cayó
                        rigs_caidos.append(rig_name)
                        print(f"  🔴 {rig_name}: {previous_status} → {rig_status}")
            
            # Guardar estados actualizados
            self.save_states()
            
            # Guardar estadísticas horarias
            self.save_hourly_stats(len(rigs), active_count, offline_count)
            
            # Resumen
            print(f"  ✓ Total: {len(rigs)} rigs")
            print(f"  ✅ Activos: {active_count}")
            print(f"  ❌ Offline: {offline_count}")
            
            # Enviar mensaje solo con estado actual (sin detalles de cambios)
            if rigs_caidos or rigs_recuperados:
                message = f"📊 <b>Reporte de Estado - {ACCOUNT_NAME}</b>\n\n"
                message += f"🕐 <b>Hora:</b> {current_time}\n\n"
                message += f"📈 <b>Estado Actual:</b>\n"
                message += f"• Total: {len(rigs)}\n"
                message += f"• Activos: {active_count}\n"
                message += f"• Offline: {offline_count}"
                
                self.notifier.send_message(message)
                print(f"  🔔 Cambios detectados: {len(rigs_caidos) + len(rigs_recuperados)}")
            else:
                print(f"  ℹ️  Sin cambios detectados")
                
        except Exception as e:
            print(f"❌ Error al verificar rigs: {e}")
            error_message = f"🚨 <b>Error en el Monitor</b>\n\n"
            error_message += f"⚠️ Error: {str(e)}\n"
            error_message += f"🕐 Hora: {get_paraguay_time().strftime('%Y-%m-%d %H:%M:%S')}"
            self.notifier.send_message(error_message)
    
    def send_status_report(self):
        """Envía un reporte del estado actual de todos los rigs"""
        try:
            rigs_data = self.client.get_rigs()
            
            if 'miningRigs' not in rigs_data:
                return
            
            rigs = rigs_data['miningRigs']
            active_rigs = [r for r in rigs if r.get('minerStatus') == 'MINING']
            offline_rigs = [r for r in rigs if r.get('minerStatus') != 'MINING']
            
            message = f"📊 <b>Reporte de Estado - {ACCOUNT_NAME}</b>\n\n"
            message += f"🕐 <b>Hora:</b> {get_paraguay_time().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            message += f"📈 <b>Total de Rigs:</b> {len(rigs)}\n"
            message += f"✅ <b>Activos:</b> {len(active_rigs)}\n"
            message += f"❌ <b>Offline:</b> {len(offline_rigs)}\n"
            
            self.notifier.send_message(message)
            print("✓ Reporte de estado enviado")
            
        except Exception as e:
            print(f"❌ Error al enviar reporte: {e}")


def main():
    """Función principal del monitor"""
    import sys
    
    # Verificar si se ejecuta en modo único (para GitHub Actions)
    check_once = '--check-once' in sys.argv
    send_report = '--send-report' in sys.argv
    daily_report = '--daily-report' in sys.argv
    
    print("\n╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "NICEHASH RIG MONITOR - TELEGRAM" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝\n")
    
    try:
        # Inicializar notificador y monitor
        notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        monitor = RigMonitor(notifier)
        
        print("✓ Monitor inicializado correctamente")
        print(f"✓ Bot de Telegram configurado")
        print(f"✓ Monitoreando {len(monitor.previous_states)} rigs\n")
        
        if daily_report:
            # Modo reporte diario: enviar resumen del día anterior
            print("📊 Modo Reporte Diario: Enviando resumen del día\n")
            monitor.send_daily_report()
            print("\n✓ Reporte diario enviado")
            return
        
        if send_report:
            # Modo reporte: solo enviar reporte de estado
            print("📊 Modo Reporte: Enviando estado del pool\n")
            monitor.send_status_report()
            print("\n✓ Reporte enviado")
            return
        
        if check_once:
            # Modo GitHub Actions: una sola verificación
            print("🔄 Modo GitHub Actions: Verificación única\n")
            monitor.check_rigs()
            print("\n✓ Verificación completada")
            return
        
        # Modo continuo: monitoreo permanente
        # Enviar mensaje de inicio
        start_message = "🤖 <b>Monitor de Rigs Iniciado</b>\n\n"
        start_message += f"✅ El bot está activo y monitoreando tus rigs\n"
        start_message += f"🕐 Inicio: {get_paraguay_time().strftime('%Y-%m-%d %H:%M:%S')}"
        notifier.send_message(start_message)
        
        # Configuración
        CHECK_INTERVAL = 60  # Segundos entre verificaciones (1 minuto)
        REPORT_INTERVAL = 3600  # Segundos entre reportes (1 hora)
        
        print(f"⏱️  Intervalo de verificación: {CHECK_INTERVAL} segundos")
        print(f"📊 Reporte automático cada: {REPORT_INTERVAL // 60} minutos")
        print("\n🔄 Iniciando monitoreo... (Presiona Ctrl+C para detener)\n")
        print("=" * 60)
        
        last_report_time = time.time()
        
        while True:
            # Verificar rigs
            monitor.check_rigs()
            
            # Enviar reporte periódico
            if time.time() - last_report_time >= REPORT_INTERVAL:
                monitor.send_status_report()
                last_report_time = time.time()
            
            # Esperar antes de la siguiente verificación
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitor detenido por el usuario")
        try:
            stop_message = "⏹️ <b>Monitor de Rigs Detenido</b>\n\n"
            stop_message += f"🕐 Fin: {get_paraguay_time().strftime('%Y-%m-%d %H:%M:%S')}"
            notifier.send_message(stop_message)
        except:
            pass
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        try:
            error_message = f"🚨 <b>Error Fatal en Monitor</b>\n\n"
            error_message += f"⚠️ {str(e)}"
            notifier.send_message(error_message)
        except:
            pass


if __name__ == "__main__":
    main()
