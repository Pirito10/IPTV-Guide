import { useState, useEffect, useMemo, useCallback } from 'react'
import { useEpg } from 'planby'
import { fetchData, getLocalDate } from '@utils'
import { theme } from '@utils/theme'

export const useApp = (selectedGroup) => {
    const [channels, setChannels] = useState([]) // Estado para los canales
    const [epg, setEpg] = useState([]) // Estado para la guía EPG
    const [isLoading, setIsLoading] = useState(true) // Estado de carga
    const [hasScrolled, setHasScrolled] = useState(false) // Estado para controlar el scroll a la hora actual

    // Variable para los datos de los canales
    const channelsData = useMemo(() => {
        // Filtramos los canales según el grupo seleccionado
        if (!selectedGroup) return channels
        return channels.filter(c => c.group === selectedGroup)
    }, [channels, selectedGroup])

    // Variable para la guía EPG
    const epgData = useMemo(() => epg, [epg])

    // Configuración de la guía de programación
    const epgProps = useEpg({
        channels: channelsData,
        epg: epgData,
        dayWidth: 10000,
        startDate: getLocalDate().split("T")[0] + "T00:00:00", // Día actual a las 00:00
        theme
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