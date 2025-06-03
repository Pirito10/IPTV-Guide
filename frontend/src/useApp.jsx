import { useState, useEffect, useMemo } from 'react'
import { useEpg } from 'planby'
import { fetchData, getTodayStart } from '@utils'
import { theme } from '@utils/theme'

const normalize = str =>
    str
        ?.normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim()


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

        const query = normalize(searchQuery)
        const result = new Set()

        // 1. Buscar coincidencias directas en canales (nombre o grupo)
        for (const channel of rawChannels) {
            const nameMatch = normalize(channel.uuid).includes(query)
            const groupMatch = normalize(channel.group).includes(query)

            if (nameMatch || groupMatch) {
                result.add(channel.uuid)
            }
        }

        // 2. Buscar coincidencias en los programas (título o descripción)
        for (const program of rawEpg) {
            if (result.has(program.channelUuid)) continue

            const title = normalize(program.title || '')
            const desc = normalize(program.description || '')

            if (title.includes(query) || desc.includes(query)) {
                result.add(program.channelUuid)
            }
        }

        // 3. Devolver solo los canales cuyos UUID están en el conjunto resultante
        return rawChannels.filter(c => result.has(c.uuid))
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
        dayWidth: 10000,
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