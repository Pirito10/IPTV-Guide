document.addEventListener("DOMContentLoaded", async function () {
    const tvGuideGrid = document.querySelector("#tv-guide");

    try {
        // Hacer la solicitud al servidor para obtener los canales
        const channelsResponse = await fetch("/api/channels");
        const channels = await channelsResponse.json();

        // Hacer la solicitud al servidor para obtener la guía EPG
        const epgResponse = await fetch("/api/epg");
        const epgData = await epgResponse.json();

        // Obtener la fecha actual en formato YYYYMMDD
        const today = new Date();
        const todayStr = today.toISOString().split("T")[0].replace(/-/g, "");

        // Si no hay canales o no hay datos de EPG, mostrar un mensaje
        if (!channels.length || Object.keys(epgData).length === 0) {
            tvGuideGrid.innerHTML = "<div class='channel-cell'>No hay datos de programación disponibles</div>";
            return;
        }

        // Calcular el número máximo de programas en un canal
        let maxPrograms = 0;
        channels.forEach(channel => {
            const channelEPG = (epgData[channel.tvg_id] || []).filter(program => program.start.startsWith(todayStr));
            if (channelEPG.length > maxPrograms) {
                maxPrograms = channelEPG.length;
            }
        });

        // Generar los datos en el grid
        channels.forEach(channel => {
            // Celda del nombre del canal
            const channelCell = document.createElement("div");
            channelCell.classList.add("channel-cell");
            channelCell.textContent = channel.name || "Canal desconocido";
            tvGuideGrid.appendChild(channelCell);

            // Obtener los programas del canal filtrados por el día actual
            const channelEPG = (epgData[channel.tvg_id] || []).filter(program => program.start.startsWith(todayStr));

            // Rellenar las celdas con los programas
            for (let i = 0; i < maxPrograms; i++) {
                const programCell = document.createElement("div");
                programCell.classList.add("program-cell");
                programCell.textContent = channelEPG[i] ? channelEPG[i].title : "-";
                tvGuideGrid.appendChild(programCell);
            }
        });

        // Ajustar el grid dinámicamente
        tvGuideGrid.style.gridTemplateColumns = `150px repeat(${maxPrograms}, 1fr)`;
    } catch (error) {
        console.error("Error al obtener los datos:", error);
        tvGuideGrid.innerHTML = "<div class='channel-cell'>Error al cargar la guía de TV</div>";
    }
});
