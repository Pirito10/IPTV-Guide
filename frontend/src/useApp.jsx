import { useState, useEffect, useMemo } from 'react'
import { useEpg } from 'planby'
import { fetchData, getTodayStart } from '@utils'
import { theme } from '@utils/theme'
import { FUSE_SEARCH_THRESHOLD, EPG_DAY_WIDTH } from '@utils/constants'
import Fuse from 'fuse.js'

export const useApp = (selectedGroups, searchQuery) => {
    const [rawChannels, setRawChannels] = useState([]) // Estado para los canales
    const [rawEpg, setRawEpg] = useState([]) // Estado para la guía EPG
    const [isLoading, setIsLoading] = useState(true) // Estado de carga
    const [hasScrolled, setHasScrolled] = useState(false) // Estado para controlar el scroll a la hora actual

    // Variable para los datos de los canales
    const channels = useMemo(() => {
        // Filtramos los canales según los grupos seleccionados si no hay una búsqueda activa
        if (searchQuery.trim() === '') {
            if (selectedGroups.length === 0) return rawChannels
            return rawChannels.filter(c => selectedGroups.includes(c.group))
        }

        // Eliminamos espacios en blanco al inicio y al final de la búsqueda
        const query = searchQuery.trim()

        // Buscamos coincidencias en los canales
        const fuseChannels = new Fuse(rawChannels, {
            keys: ['uuid', 'group', 'streams.name'],
            threshold: FUSE_SEARCH_THRESHOLD,
        })
        // Guardamos los UUIDs de los canales que coinciden
        const matchedChannelUUIDs = new Set(
            fuseChannels.search(query).map(r => r.item.uuid)
        )

        // Buscamos coincidencias en los programas
        const fusePrograms = new Fuse(rawEpg, {
            keys: ['title', 'description'],
            threshold: FUSE_SEARCH_THRESHOLD,
        })
        // Guardamos los UUIDs de los canales de los programas que coinciden
        fusePrograms.search(query).forEach(r => {
            matchedChannelUUIDs.add(r.item.channelUuid)
        })

        // Filtramos los canales originales por los UUIDs seleccionados
        return rawChannels.filter(c => matchedChannelUUIDs.has(c.uuid))
    }, [rawChannels, selectedGroups, searchQuery])

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
        dayWidth: EPG_DAY_WIDTH,
        startDate: getTodayStart(),
        theme: theme
    })

    // Función para cargar los datos de los canales y la guía EPG
    const loadInitialData = async () => {
        setIsLoading(true)
        const { channels: rawChannels, epg: rawEpg } = await fetchData()
        setRawChannels(rawChannels)
        setRawEpg(rawEpg)
        setIsLoading(false)
    }

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