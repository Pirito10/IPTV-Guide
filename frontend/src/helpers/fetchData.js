import { formatChannels, formatEpg } from './formatData'

// Función para obtener los datos de los canales y la guía EPG del backend
export const fetchData = async () => {
    try {
        // Hacemos las peticiones a la API
        const [channelsResponse, epgResponse] = await Promise.all([
            fetch("http://127.0.0.1:5000/api/channels"),
            fetch("http://127.0.0.1:5000/api/epg")
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