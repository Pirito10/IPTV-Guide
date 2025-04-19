import React, { useState } from 'react'
import { Epg, Layout } from 'planby'
import { useApp } from '@/useApp'
import { Timeline, ChannelItem, ChannelModal, ProgramItem, ProgramModal } from '@components'
import '@styles/global.css'

const App = () => {
    // Obtenemos los datos y propiedades de la guía de programación
    const { epgProps, isLoading } = useApp()

    const [selectedChannel, setSelectedChannel] = useState(null) // Estado para el canal seleccionado
    const [selectedProgram, setSelectedProgram] = useState(null) // Estado para el programa seleccionado

    // Renderizamos el HTML de la guía de programación
    return (
        <div style={{ height: "100%", width: "100%" }}>
            <Epg isLoading={isLoading} {...epgProps.getEpgProps()} style={{ padding: 0 }} >
                <Layout
                    {...epgProps.getLayoutProps()}
                    renderTimeline={(props) => <Timeline {...props} />}
                    renderChannel={(props) => <ChannelItem key={props.channel.uuid} channel={props.channel} onClick={() => setSelectedChannel(props.channel)} />}
                    renderProgram={(props) => <ProgramItem key={props.program.data.id} onClick={() => setSelectedProgram(props.program.data)} {...props} />}
                />
            </Epg>
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