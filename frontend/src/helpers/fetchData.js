import { formatChannels, formatEpg } from './formatData'

// Función para obtener los datos de los canales y la guía EPG del backend
export const fetchData = async () => {
    try {
        // Hacemos las peticiones a la API
        const [channelsResponse, epgResponse] = await Promise.all([
            fetch("http://pirito10.duckdns.org/api/channels"),
            fetch("http://pirito10.duckdns.org/api/epg")
        ])

        if (!channelsResponse.ok || !epgResponse.ok) {
            throw new Error(`Error en la carga de datos: ${channelsResponse.status}, ${epgResponse.status}`)
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