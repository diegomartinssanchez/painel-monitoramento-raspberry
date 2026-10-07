from datetime import datetime

from pydantic import BaseModel


class Host(BaseModel):
    nome: str
    ip: str
    sistema: str
    uptime: str


class Cpu(BaseModel):
    uso_percentual: float
    temperatura: float | None
    nucleos: int


class Memoria(BaseModel):
    total_mb: float
    usada_mb: float
    percentual: float


class Armazenamento(BaseModel):
    total_gb: float
    usado_gb: float
    livre_gb: float
    percentual: float


class InfosRaspberry(BaseModel):
    status: str
    timestamp: datetime
    host: Host
    cpu: Cpu
    memoria: Memoria
    armazenamento: Armazenamento