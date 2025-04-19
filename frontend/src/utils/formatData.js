import { FALLBACK_LOGO, DEFAULT_GROUP } from "@utils/constants"

// Función para formatear los canales al formato de Planby
export const formatChannels = (channelsData) => {
    const channels = [] // Lista de canales en formato de Planby

    // Recorremos la lista de canales de la API
    channelsData.forEach((channel) => {
        // Obtenemos los datos del canal
        const { id, logo, group, streams } = channel

        // Añadimos el canal a la lista
        channels.push({
            uuid: id,
            logo: logo || FALLBACK_LOGO,
            group: group || DEFAULT_GROUP,
            streams: streams
        })
    })

    return channels
}

// Función para formatear la guía EPG al formato de Planby
export const formatEpg = (epg, channels) => {
    return channels.flatMap(channel => {
        // Buscamos los programas asociados a este canal
        const programs = epg[channel.uuid]?.programs || []

        // Generamos las entradas de la guía EPG
        return programs.map(program => ({
            id: `${channel.uuid}~${program.since}`,
            channelUuid: channel.uuid,
            title: program.title,
            description: program.description,
            since: new Date(program.since).toISOString(),
            till: new Date(program.till).toISOString()
        }))
    })
};