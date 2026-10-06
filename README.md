# Painel Web de Monitoramento da Raspberry Pi

Aplicação desenvolvida para monitoramento de recursos de hardware em tempo real de um nó Raspberry Pi conectado à rede local.

## Funcionalidades
- Leitura em tempo real de CPU, Temperatura, RAM, Disco e Uptime.
- API REST entregando métricas em JSON (`/api/status`).
- Interface responsiva com polling automático a cada 5 segundos e alertas visuais.

## Como Executar
1. Instale as dependências: `pip install flask psutil --break-system-packages`
2. Inicie a aplicação: `python3 app.py`
3. Acesse via navegador: `http://<IP_DA_RASPBERRY>:5000`
