import os
import platform
import socket
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)


def obter_ip_local() -> str:
    """Obtém o IP local da Raspberry Pi na rede local."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def obter_temperatura_cpu() -> float | None:
    """Lê a temperatura nativa da CPU da Raspberry Pi via sysfs Linux."""
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
    """Formata o tempo decorrido desde a inicialização (uptime)."""
    segundos_ativos = int(time.time() - boot_timestamp)
    delta = timedelta(seconds=segundos_ativos)
    dias = delta.days
    horas, resto = divmod(delta.seconds, 3600)
    minutos, segundos = divmod(resto, 60)

    if dias > 0:
        return f"{dias}d {horas:02d}h {minutos:02d}m {segundos:02d}s"
    return f"{horas:02d}h {minutos:02d}m {segundos:02d}s"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def api_status():
    try:
        uso_disco = psutil.disk_usage("/")
        uso_memoria = psutil.virtual_memory()
        boot_time = psutil.boot_time()

        dados = {
            "status": "sucesso",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "host": {
                "nome": socket.gethostname(),
                "ip": obter_ip_local(),
                "sistema": f"{platform.system()} {platform.release()} ({platform.machine()})",
                "uptime": obter_tempo_atividade(boot_time),
            },
            "cpu": {
                "uso_percentual": psutil.cpu_percent(interval=0.5),
                "temperatura": obter_temperatura_cpu(),
                "nucleos": psutil.cpu_count(logical=True),
            },
            "memoria": {
                "total_mb": round(uso_memoria.total / (1024 * 1024), 1),
                "usada_mb": round(uso_memoria.used / (1024 * 1024), 1),
                "percentual": uso_memoria.percent,
            },
            "armazenamento": {
                "total_gb": round(uso_disco.total / (1024**3), 2),
                "usado_gb": round(uso_disco.used / (1024**3), 2),
                "livre_gb": round(uso_disco.free / (1024**3), 2),
                "percentual": uso_disco.percent,
            },
        }
        return jsonify(dados), 200
    except Exception as erro:
        return jsonify({"status": "erro", "mensagem": str(erro)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
