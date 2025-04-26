import { formatChannels, formatEpg } from '@utils'
import { CHANNELS_URL, EPG_URL } from '@utils/constants'

// Función para obtener los datos de los canales y la guía EPG del backend
export const fetchData = async () => {
    try {
        // Hacemos las peticiones a la API
        const channelsResponse = await fetch(CHANNELS_URL)
        const epgResponse = await fetch(EPG_URL)

        // Comprobamos si la respuesta para los canales es correcta
        if (!channelsResponse.ok) {
            // Si no es correcta, lanzamos un error y no se devuelven los datos
            throw new Error(`\nNo se han podido descargar los canales: ${channelsResponse.status} - ${channelsResponse.statusText}`)
        }
        // Comprobamos si la respuesta para la EPG es correcta
        try {
            if (!epgResponse.ok) {
                // Si no es correcta, lanzamos un error y solo se devuelven los datos de los canales
                throw new Error(`\nNo se ha podido descargar la EPG: ${epgResponse.status} - ${epgResponse.statusText}`)
            }
        } catch (error) {
            console.error("Error obteniendo los datos del servidor", error.message)
        }

        // Convertimos los datos a formato JSON
        const channelsData = await channelsResponse.json()
        const epgData = await epgResponse.json()

        // Convertimos los datos al formato de Planby
        const channels = formatChannels(channelsData)
        const epg = formatEpg(epgData, channels)

        return { channels, epg }
    } catch (error) {
        console.error("Error obteniendo los datos del servidor:", error.message)
        return { channels: [], epg: [] }
    }
}