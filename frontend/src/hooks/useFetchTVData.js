import { useEffect, useState } from 'react'

// Hook para obtener los datos de los canales y la guía EPG
export const useFetchTVData = () => {
    const [channels, setChannels] = useState([]) // Variables para los canales
    const [epg, setEpg] = useState([]) // Variables para la guía EPG
    const [loading, setLoading] = useState(true) // Variables para el estado de cargando, activo por defecto

    // Se ejecuta al montar el componente
    useEffect(() => {
        // Función que obtiene los datos de los canales y la guía EPG
        async function fetchData() {
            try {
                // Solicitamos los datos de los canales y la guía EPG al backend
                const [channelsResponse, epgResponse] = await Promise.all([
                    fetch("http://localhost:5000/api/channels"),
                    fetch("http://localhost:5000/api/epg")
                ])

                if (!channelsResponse.ok || !epgResponse.ok) {
                    throw new Error("Error en la carga de datos")
                }

                // Convertimos los datos a formato JSON
                const [channelsData, epgData] = await Promise.all([
                    channelsResponse.json(),
                    epgResponse.json()
                ])

                // Actualizamos el estado de los canales y la guía EPG
                setChannels(channelsData)
                setEpg(epgData)
            } catch (error) {
                console.error("Error obteniendo los datos:", error)
            } finally {
                // Desactivamos el estado de cargando
                setLoading(false)
            }
        }

        // Ejecutamos la función para obtener los datos
        fetchData()
    }, [])

    // Devolvemos los canales, la guía EPG y el estado de cargando
    return { channels, epg, loading }
}