import React from 'react'
import { Epg, Layout } from 'planby'
import { useApp } from './useApp'
import { Timeline, ChannelItem, ProgramItem } from './components'

const App = () => {
    // Obtenemos los datos y propiedades de la guía de programación
    const { epgProps, isLoading } = useApp()

    // Renderizamos el HTML de la guía de programación
    return (
        <div style={{ height: "80vh" }}>
            <Epg isLoading={isLoading} {...epgProps.getEpgProps()} >
                <Layout
                    {...epgProps.getLayoutProps()}
                    renderTimeline={(props) => <Timeline {...props} />}
                    renderChannel={(props) => <ChannelItem key={props.channel.uuid} channel={props.channel} />}
                    renderProgram={(props) => <ProgramItem key={props.program.data.id} {...props} />}
                />
            </Epg>
        </div>
    )
}

export default App