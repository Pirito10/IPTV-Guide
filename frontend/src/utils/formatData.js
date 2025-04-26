import { FALLBACK_LOGO, DEFAULT_GROUP } from '@utils/constants'

// Función para formatear los canales al formato de Planby
export const formatChannels = (channelsData) =>
    // Recorremos la lista de canales y los transformamos al formato de Planby
    channelsData.map(({ id, logo, group, streams }) => ({
        uuid: id,
        logo: logo || FALLBACK_LOGO,
        group: group || DEFAULT_GROUP,
        streams
    }))


// Función para formatear la guía EPG al formato de Planby
export const formatEpg = (epg, channels) =>
    // Recorremos la lista por canales
    channels.flatMap(channel => {
        // Buscamos los programas asociados a este canal
        const programs = epg[channel.uuid]?.programs || []

        // Generamos una lista de programas en el formato de Planby
        return programs.map(program => ({
            id: `${channel.uuid}~${program.since}`,
            channelUuid: channel.uuid,
            title: program.title,
            description: program.description,
            since: new Date(program.since).toISOString(),
            till: new Date(program.till).toISOString()
        }))
    })