import { useState } from 'react'
import { Epg, Layout } from 'planby'
import { useApp } from '@/useApp'
import { Toolbar, Timeline, ChannelItem, ChannelModal, ProgramItem, ProgramModal } from '@components'

const App = () => {
    const [selectedChannel, setSelectedChannel] = useState(null) // Estado para el canal seleccionado
    const [selectedProgram, setSelectedProgram] = useState(null) // Estado para el programa seleccionado
    const [selectedGroups, setSelectedGroups] = useState([]) // Estado para los grupos seleccionados
    const [searchQuery, setSearchQuery] = useState('') // Estado para la búsqueda de canales
    const [isFiltering, setIsFiltering] = useState(false) // Estado de carga por filtrado

    // Obtenemos los datos y propiedades de la guía de programación
    const { epgProps, isLoading, groups } = useApp(selectedGroups)

    // Obtenemos la altura de la barra de herramientas
    const toolbarHeight = getComputedStyle(document.documentElement).getPropertyValue('--toolbar-height')

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

    const handleQueryChange = (query) => {
        setSearchQuery(query);
    }

    return (
        <div id="epg-root">
            <Toolbar groups={groups} selectedGroups={selectedGroups} onGroupChange={handleGroupChange} searchQuery={searchQuery} onQueryChange={handleQueryChange} />
            <div style={{ height: `calc(100% - ${toolbarHeight})` }}>
                <Epg style={{ padding: 0 }} isLoading={isLoading || isFiltering} {...epgProps.getEpgProps()}  >
                    <Layout
                        {...epgProps.getLayoutProps()}
                        renderTimeline={props => <Timeline {...props} />}
                        renderChannel={props => <ChannelItem key={props.channel.uuid} channel={props.channel} onClick={() => setSelectedChannel(props.channel)} />}
                        renderProgram={props => <ProgramItem key={props.program.data.id} program={props.program} onClick={() => setSelectedProgram(props.program.data)} />}
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