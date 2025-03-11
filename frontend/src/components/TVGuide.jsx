import React, { useEffect, useState, useMemo } from 'react';
import { useEpg, Epg, Layout } from 'planby'

const TVGuide = () => {
    const [channels, setChannels] = useState([]); // Almacenará los canales
    const [epg, setEpg] = useState([]); // Almacenará la guía de TV
    const [loading, setLoading] = useState(true); // Para mostrar "Cargando..."

    useEffect(() => {
        async function fetchData() {
            try {
                const [channelsResponse, epgResponse] = await Promise.all([
                    fetch("http://localhost:5000/api/channels"),
                    fetch("http://localhost:5000/api/epg")
                ]);

                if (!channelsResponse.ok || !epgResponse.ok) {
                    throw new Error("Error en la carga de datos");
                }

                const [channelsData, epgData] = await Promise.all([
                    channelsResponse.json(),
                    epgResponse.json()
                ]);

                setChannels(channelsData);
                setEpg(epgData);
            } catch (error) {
                console.error("Error obteniendo los datos:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, []); // Se ejecuta solo al montar el componente

    // 📌 Formatear los canales y programas correctamente
    const formattedChannels = useMemo(() => {
        return channels.map(channel => ({
            uuid: channel.tvg_id,
            logo: channel.logo || "https://via.placeholder.com/100x50",
            name: channel.name,
        }));
    }, [channels]);

    const formattedEpg = useMemo(() => {
        return Object.entries(epg).flatMap(([channelUuid, programs]) =>
            programs.map(program => ({
                id: `${channelUuid}-${program.start}`,
                channelUuid,
                title: program.title,
                since: new Date(program.start).toISOString(),
                till: new Date(program.stop).toISOString(),
                image: "https://via.placeholder.com/150x100",
            }))
        );
    }, [epg]);

    // 📌 Mover useEpg fuera del useEffect y definirlo en el cuerpo del componente
    const epgProps = useEpg({
        epg: formattedEpg,
        channels: formattedChannels,
        startDate: new Date().toISOString().split("T")[0], // Fecha actual
        width: 1200,
        height: 600,
    });

    // Mientras carga, mostramos un mensaje
    if (loading) return <p>Cargando datos...</p>;

    // Si no hay datos, mostramos un mensaje de error
    if (!channels.length || Object.keys(epg).length === 0) return <p>No hay datos disponibles.</p>;

    return (
        <div>
            <div style={{ height: "600px", width: "1200px" }}>
                <Epg {...epgProps.getEpgProps()}>
                    <Layout {...epgProps.getLayoutProps()} />
                </Epg>
            </div>
        </div>
    );
};

export default TVGuide;