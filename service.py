import socket
import time
import psutil
import os
from datetime import datetime, timedelta

def obter_ip_local() -> str:
    """Obtém o IP local da Raspberry Pi na rede local."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def obter_temperatura_cpu() -> float | None:
    caminho_termico = "/sys/class/thermal/thermal_zone0/temp"
    try:
        if os.path.exists(caminho_termico):
            with open(caminho_termico, "r", encoding="utf-8") as f:
                return round(float(f.read().strip()) / 1000.0, 1)

        temps = getattr(psutil, "sensors_temperatures", lambda: {})()
        if "cpu_thermal" in temps and temps["cpu_thermal"]:
            return round(temps["cpu_thermal"][0].current, 1)
    except Exception:
        pass
    return None


def obter_tempo_atividade(boot_timestamp: float) -> str:
    segundos_ativos = int(time.time() - boot_timestamp)
    delta = timedelta(seconds=segundos_ativos)
    dias = delta.days
    horas, resto = divmod(delta.seconds, 3600)
    minutos, segundos = divmod(resto, 60)

    if dias > 0:
        return f"{dias}d {horas:02d}h {minutos:02d}m {segundos:02d}s"
    return f"{horas:02d}h {minutos:02d}m {segundos:02d}s"


def obter_uso_cpu():
    return psutil.cpu_percent(interval=0.5)

def obter_uso_memoria():
    memoria = psutil.virtual_memory()
    return round(memoria.used / (1024 * 1024), 1)

def obter_memoria_total():
    memoria = psutil.virtual_memory()
    return round(memoria.total / (1024 * 1024), 1)

def obter_uso_disco():
    disco = psutil.disk_usage('/')
    return round(disco.used / (1024**3), 2)

def obter_disco_total():
    disco = psutil.disk_usage('/')
    return round(disco.total / (1024**3), 2)

def obter_disco_livre():
    disco = psutil.disk_usage('/')
    return round(disco.free / (1024**3), 2)

def obter_dt_ult_att():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")