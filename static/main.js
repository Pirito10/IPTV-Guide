function generateTimeline() {
    const timeline = document.getElementById("timeline");
    for (let i = 0; i < 24; i++) {
        const hourBlock = document.createElement("div");
        hourBlock.textContent = i.toString().padStart(2, '0') + ":00";
        timeline.appendChild(hourBlock);
    }
}

async function fetchChannels() {
    const response = await fetch('/api/channels');
    const channels = await response.json();
    const channelList = document.getElementById("channel-list");
    channelList.innerHTML = "";

    channels.forEach(channel => {
        const channelDiv = document.createElement("div");
        channelDiv.classList.add("channel");
        channelDiv.innerHTML = `
            <img src="${channel.logo}" alt="Logo">
            <span onclick="copyToClipboard('${channel.url}')">${channel.name}</span>
        `;
        channelList.appendChild(channelDiv);
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert("Enlace copiado: " + text);
    }).catch(err => {
        console.error("Error al copiar: ", err);
    });
}

generateTimeline();
fetchChannels();