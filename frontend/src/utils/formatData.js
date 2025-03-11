// Función para formatear los canales al formato de Planby
export const formatChannels = (channels) => {
    const uniqueChannels = [] // Lista de canales formateados
    const channelCount = {} // Contador de canales con el mismo ID

    // Recorremos la lista de canales
    channels.forEach((channel) => {
        // Obtenemos los datos del canal
        const { tvg_id, logo, name, url } = channel

        // Si un canal con el mismo ID ya existe, incrementamos el contador para ese ID
        if (channelCount[tvg_id]) {
            channelCount[tvg_id] += 1
        } else {
            channelCount[tvg_id] = 1
        }

        // Generamos un ID único para el canal
        const uniqueId = `${tvg_id}-${channelCount[tvg_id]}`

        // Añadimos el canal a la lista
        uniqueChannels.push({
            uuid: uniqueId,
            logo: logo || "/tebas.jpg",
            name: name || "Canal desconocido",
            url: url,
        })
    })

    return uniqueChannels
}

// Función para formatear la guía EPG al formato de Planby
export const formatEpg = (epg, formattedChannels) => {
    // Recorremos la guía EPG y generamos un objeto con los programas de cada canal
    return Object.entries(epg).flatMap(([channelUuid, programs]) => {
        // Filtramos los canales formateados que coincidan con el ID del canal
        const matchingChannels = formattedChannels.filter(c => c.uuid.startsWith(channelUuid))

        // Por cada canal, generamos un objeto con los programas
        return matchingChannels.flatMap(channel =>
            programs.map(program => ({
                id: `${channel.uuid}-${program.start}`,
                channelUuid: channel.uuid,
                title: program.title,
                since: new Date(program.start).toISOString(),
                till: new Date(program.stop).toISOString(),
                image: "/tebas.jpg",
            }))
        )
    })
}