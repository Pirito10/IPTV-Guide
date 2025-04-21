import React, { useState, useEffect } from 'react'
import { Epg, Layout } from 'planby'
import { useApp } from '@/useApp'
import { Toolbar, Timeline, ChannelItem, ChannelModal, ProgramItem, ProgramModal } from '@components'
import '@styles/global.css'

const App = () => {
    const [selectedChannel, setSelectedChannel] = useState(null) // Estado para el canal seleccionado
    const [selectedProgram, setSelectedProgram] = useState(null) // Estado para el programa seleccionado
    const [selectedGroups, setSelectedGroups] = useState(null) // Estado para el grupo seleccionado
    const [isFiltering, setIsFiltering] = useState(false) // Estado de carga por filtrado

    // Obtenemos los datos y propiedades de la guía de programación
    const { epgProps, isLoading, groups } = useApp(selectedGroups)

    // Obtenemos la altura de la barra de herramientas
    const toolbarHeight = getComputedStyle(document.documentElement).getPropertyValue('--toolbar-height')

    // Establecemos todos los grupos como seleccionados por defecto
    useEffect(() => {
        if (groups.length > 0) {
            setSelectedGroups(groups)
        }
    }, [groups])

    // Función para manejar el cambio de grupo seleccionado
    const handleGroupChange = (newGroups) => {
        // Marcamos el inicio del filtrado para mostrar una animación
        setIsFiltering(true)

        // Reservamos un frame para mostrar la animación
        requestAnimationFrame(() => {
            // Actualizamos el estado de los grupos seleccionados
            setSelectedGroups(newGroups)

            // Marcamos el fin del filtrado después de un tiempo
            setTimeout(() => {
                setIsFiltering(false)
            }, 300)
        })
    }

    // Renderizamos el HTML de la guía de programación
    return (
        <div id="epg-root">
            <Toolbar groups={groups} selectedGroups={selectedGroups} onGroupChange={handleGroupChange} />
            <div style={{ height: `calc(100% - ${toolbarHeight})` }}>
                <Epg isLoading={isLoading || isFiltering} {...epgProps.getEpgProps()} style={{ padding: 0 }} >
                    <Layout
                        {...epgProps.getLayoutProps()}
                        renderTimeline={(props) => <Timeline {...props} />}
                        renderChannel={(props) => <ChannelItem key={props.channel.uuid} channel={props.channel} onClick={() => setSelectedChannel(props.channel)} />}
                        renderProgram={(props) => <ProgramItem key={props.program.data.id} onClick={() => setSelectedProgram(props.program.data)} {...props} />}
                    />
                </Epg>
            </div>
            {selectedChannel && <ChannelModal channel={selectedChannel} onClose={() => setSelectedChannel(null)} />}
            {selectedProgram &&
                <ProgramModal
                    program={selectedProgram}
                    // Buscamos el logo del canal correspondiente al programa
                    logo={
                        epgProps.getLayoutProps().channels.find(
                            c => c.uuid === selectedProgram.channelUuid
                        )?.logo
                    }
                    onClose={() => setSelectedProgram(null)}
                />
            }
        </div>
    )
}

export default App