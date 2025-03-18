import { useState, useEffect, useMemo, useCallback } from 'react'
import { useEpg } from 'planby'
import { fetchData } from './helpers'

export const useApp = () => {
    const [channels, setChannels] = useState([]) // Estado para los canales
    const [epg, setEpg] = useState([]) // Estado para la guía EPG
    const [isLoading, setIsLoading] = useState(true) // Estado de carga
    const [hasScrolled, setHasScrolled] = useState(false) // Estado para controlar el scroll a la hora actual

    // Variables para los datos de los canales y la guía EPG en formato de Planby
    const channelsData = useMemo(() => channels, [channels])
    const epgData = useMemo(() => epg, [epg])

    // Configuración de la guía de programación
    const epgProps = useEpg({
        channels: channelsData,
        epg: epgData,
        width: 1850,
        height: 900,
        dayWidth: 10000,
        startDate: new Date().toISOString().split("T")[0] + "T00:00:00", // Fecha actual
    })

    // Función para cargar los datos de los canales y la guía EPG
    const handleFetchResources = useCallback(async () => {
        setIsLoading(true)
        const { channels, epg } = await fetchData()
        setChannels(channels)
        setEpg(epg)
        setIsLoading(false)
    }, [])

    // Ejecutamos la carga de datos al montar el componente
    useEffect(() => {
        handleFetchResources()
    }, [handleFetchResources])

    // Ejecutamos un scroll a la hora actual
    useEffect(() => {
        if (!hasScrolled && epgProps.onScrollToNow) {
            epgProps.onScrollToNow()
            setHasScrolled(true)
        }
    }, [hasScrolled, epgProps])

    return { epgProps, isLoading }
}