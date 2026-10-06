async function carregarStatus() {
    const btn = document.getElementById("btn-atualizar");
    btn.disabled = true;
    btn.textContent = "Lendo...";

    try {
        const response = await fetch("/api/status");
        if (!response.ok) throw new Error("Erro na comunicação com o servidor.");

        const data = await response.json();

        document.getElementById("hostname").textContent = data.host.nome;
        document.getElementById("ip-address").textContent = data.host.ip;
        document.getElementById("uptime").textContent = data.host.uptime;
        document.getElementById("last-update").textContent = data.timestamp;

        const cpuPct = data.cpu.uso_percentual;
        document.getElementById("cpu-percent").textContent = `${cpuPct}%`;
        ajustarBarra("cpu-bar", cpuPct);

        const temp = data.cpu.temperatura;
        const tempEl = document.getElementById("cpu-temp");
        if (temp !== null) {
            tempEl.textContent = `${temp} °C`;
            tempEl.className = temp >= 75 ? "level-critical" : (temp >= 60 ? "level-warning" : "level-normal");
        } else {
            tempEl.textContent = "N/D";
        }

        const ramPct = data.memoria.percentual;
        document.getElementById("ram-percent").textContent = `${ramPct}%`;
        document.getElementById("ram-used").textContent = data.memoria.usada_mb;
        document.getElementById("ram-total").textContent = data.memoria.total_mb;
        ajustarBarra("ram-bar", ramPct);

        const diskPct = data.armazenamento.percentual;
        document.getElementById("disk-percent").textContent = `${diskPct}%`;
        document.getElementById("disk-used").textContent = data.armazenamento.usado_gb;
        document.getElementById("disk-total").textContent = data.armazenamento.total_gb;
        ajustarBarra("disk-bar", diskPct);

    } catch (err) {
        console.error("Falha ao coletar dados:", err);
    } finally {
        btn.disabled = false;
        btn.textContent = "Atualizar Agora";
    }
}

function ajustarBarra(elementId, percent) {
    const el = document.getElementById(elementId);
    el.style.width = `${percent}%`;

    el.classList.remove("level-normal", "level-warning", "level-critical");

    if (percent >= 85) {
        el.classList.add("level-critical");
    } else if (percent >= 70) {
        el.classList.add("level-warning");
    } else {
        el.classList.add("level-normal");
    }
}

carregarStatus();
setInterval(carregarStatus, 5000);
