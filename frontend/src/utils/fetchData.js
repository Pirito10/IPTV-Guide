import { formatChannels, formatEpg } from '@utils/formatData'
import { CHANNELS_URL, EPG_URL } from '@utils/constants'

// Función para obtener los datos de los canales y la guía EPG del backend
export const fetchData = async () => {
    try {
        // Hacemos las peticiones a la API
        const [channelsResponse, epgResponse] = await Promise.all([
            fetch(CHANNELS_URL),
            fetch(EPG_URL)
        ])

        if (!channelsResponse.ok) {
            throw new Error(`\nNo se han podido descargar los canales: ${channelsResponse.status} - ${channelsResponse.statusText}`)
        }

        if (!epgResponse.ok) {
            throw new Error(`\nNo se ha podido descargar la EPG: ${epgResponse.status} - ${epgResponse.statusText}`)
        }

        // Convertimos los datos a formato JSON
        const [channelsData, epgData] = await Promise.all([
            channelsResponse.json(),
            epgResponse.json()
        ])

        // Convertimos los datos al formato de Planby
        const channels = formatChannels(channelsData)
        const epg = formatEpg(epgData, channels)

        return { channels, epg }
    } catch (error) {
        console.error("Error obteniendo los datos:", error)
        return { channels: [], epg: [] }
    }
}