document.addEventListener("DOMContentLoaded", async function () {
    const channelsContainer = document.getElementById("channels-container");

    try {
        const response = await fetch("/api/channels");
        const channels = await response.json();

        channels.forEach(channel => {
            const row = document.createElement("div");
            row.classList.add("channel-row");

            const logo = document.createElement("img");
            logo.src = channel.logo;
            logo.alt = channel.name;
            logo.classList.add("channel-logo");

            const name = document.createElement("span");
            name.textContent = channel.name;
            name.classList.add("channel-name");

            row.appendChild(logo);
            row.appendChild(name);
            channelsContainer.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading channels:", error);
    }
});
