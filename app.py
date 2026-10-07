import platform
import socket
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
import psutil
import uvicorn
from fastapi.templating import Jinja2Templates


from entity import Cpu, Host, InfosRaspberry, Memoria, Armazenamento
from service import obter_disco_livre, obter_disco_total, obter_ip_local, obter_memoria_total, obter_temperatura_cpu, obter_tempo_atividade, obter_uso_cpu, obter_uso_disco, obter_uso_memoria

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request,name="index.html",context={"request": request})


@app.get("/api/status", response_model=InfosRaspberry)
def api_status():
    try:
        uso_disco = psutil.disk_usage("/")
        uso_memoria = psutil.virtual_memory()
        boot_time = psutil.boot_time()

        return InfosRaspberry(
            status="sucesso",
            timestamp=datetime.now(),
            host=Host(
                nome=socket.gethostname(),
                ip=obter_ip_local(),
                sistema=f"{platform.system()} {platform.release()} ({platform.machine()})",
                uptime=obter_tempo_atividade(boot_time),
            ),
            cpu=Cpu(
                uso_percentual=obter_uso_cpu(),
                temperatura=obter_temperatura_cpu(),
                nucleos=psutil.cpu_count(logical=True),
            ),
            memoria=Memoria(
                total_mb=obter_memoria_total(),
                usada_mb=obter_uso_memoria(),
                percentual=uso_memoria.percent,
            ),
            armazenamento=Armazenamento(
                total_gb=obter_disco_total(),
                usado_gb=obter_uso_disco(),
                livre_gb=obter_disco_livre(),
                percentual=uso_disco.percent,
            ),
        )
    except Exception as erro:
        print(f"ERRO: {type(erro).__name__}: {erro}")
        raise HTTPException(status_code=500,detail=str(erro))