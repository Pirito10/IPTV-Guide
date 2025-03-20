// Función para formatear los canales al formato de Planby
export const formatChannels = (channelsData) => {
    const channels = [] // Lista de canales en formato de Planby

    // Recorremos la lista de canales de la API
    channelsData.forEach((channel) => {
        // Obtenemos los datos del canal
        const { id, logo, name, url } = channel

        // Añadimos el canal a la lista
        channels.push({
            uuid: id,
            logo: logo,
            name: name,
            url: url,
        })
    })

    return channels
}

// Función para formatear la guía EPG al formato de Planby
export const formatEpg = (epg, channels) => {
    return channels.flatMap(channel => {
        // Eliminamos el contador del ID del canal
        const channelID = channel.uuid.split("#")[0];

        // Buscamos los programas asociados a este canal
        const programs = epg[channelID] || [];

        // Generamos las entradas de la guía EPG
        return programs.map(program => ({
            id: `${channel.uuid}~${program.start}`,
            channelUuid: channel.uuid,
            title: program.title,
            description: program.description,
            since: new Date(program.start).toISOString(),
            till: new Date(program.stop).toISOString()
        }));
    });
};