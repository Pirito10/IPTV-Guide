import { useState, useEffect, useMemo, useCallback } from 'react'
import { useEpg } from 'planby'
import { fetchData, getTodayStart } from '@utils'
import { theme } from '@utils/theme'

export const useApp = (selectedGroups) => {
    const [rawChannels, setRawChannels] = useState([]) // Estado para los canales
    const [rawEpg, setRawEpg] = useState([]) // Estado para la guía EPG
    const [isLoading, setIsLoading] = useState(true) // Estado de carga
    const [hasScrolled, setHasScrolled] = useState(false) // Estado para controlar el scroll a la hora actual

    // Variable para los datos de los canales
    const channels = useMemo(() => {
        // Filtramos los canales según el grupo seleccionado
        if (!selectedGroups) return rawChannels
        return rawChannels.filter(c => selectedGroups.includes(c.group))
    }, [rawChannels, selectedGroups])

    // Variable para los datos de la guía EPG
    const epg = rawEpg

    // Lista con los grupos de los canales
    const groups = useMemo(() => {
        return [...new Set(rawChannels.map(c => c.group))]
    }, [rawChannels])

    // Configuración de la guía de programación
    const epgProps = useEpg({
        channels: channels,
        epg: epg,
        dayWidth: 10000,
        startDate: getTodayStart(),
        theme
    })

    // Función para cargar los datos de los canales y la guía EPG en el primer renderizado
    const loadInitialData = useCallback(async () => {
        setIsLoading(true)
        const { channels: rawChannels, epg: rawEpg } = await fetchData()
        setRawChannels(rawChannels)
        setRawEpg(rawEpg)
        setIsLoading(false)
    }, [])

    // Ejecutamos la carga de datos al montar el componente
    useEffect(() => {
        loadInitialData()
    }, [])

    // Ejecutamos un scroll a la hora actual
    useEffect(() => {
        if (!hasScrolled) {
            epgProps.onScrollToNow()
            setHasScrolled(true)
        }
    }, [hasScrolled])

    return { epgProps, isLoading, groups }
}