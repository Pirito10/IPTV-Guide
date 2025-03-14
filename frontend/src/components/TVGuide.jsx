import React, { useMemo, useEffect, useState } from 'react'
import { useEpg, Epg, Layout } from 'planby'
import { useFetchTVData } from '../hooks/useFetchTVData'
import { formatChannels, formatEpg } from '../utils/formatData'

// Componente con la guía de TV
const TVGuide = () => {
    // Obtenemos los datos de los canales y programas del backend
    const { channels, epg, loading } = useFetchTVData()

    // Estado para saber si ya se ha hecho scroll a la hora actual
    const [hasScrolled, setHasScrolled] = useState(false)

    // Formateamos los datos de los canales y programas al formato de Planby
    const formattedChannels = useMemo(() => formatChannels(channels), [channels]);
    const formattedEpg = useMemo(() => formatEpg(epg, formattedChannels), [epg, formattedChannels]);

    // Configuración de Planby
    const epgProps = useEpg({
        epg: formattedEpg,
        channels: formattedChannels,
        width: 1850,
        height: 900,
        dayWidth: 10000,
        startDate: new Date().toISOString().split("T")[0] + "T00:00:00", // Fecha actual
    });

    // Ejecutamos un scroll a la hora actual
    useEffect(() => {
        if (!hasScrolled && epgProps.onScrollToNow) {
            epgProps.onScrollToNow();
            setHasScrolled(true)
        }
    }, [hasScrolled, epgProps]);

    // Mientras carga, mostramos un mensaje
    if (loading) return <p>Cargando datos...</p>;

    // Si no hay datos, mostramos un mensaje de error
    if (!channels.length || Object.keys(epg).length === 0) return <p>No hay datos disponibles.</p>;

    // Devolvemos el HTML con la guía de TV
    return (
        <div>
            <Epg {...epgProps.getEpgProps()} >
                <Layout {...epgProps.getLayoutProps()} />
            </Epg>
        </div>
    );
};

export default TVGuide;