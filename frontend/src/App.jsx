import React from 'react'
import { Epg, Layout } from 'planby'
import { useApp } from './useApp'
import { ProgramItem } from './components'

const App = () => {
    // Obtenemos los datos y propiedades de la guía de programación
    const { epgProps, isLoading } = useApp();

    // Renderizamos el HTML de la guía de programación
    return (
        <div>
            <Epg isLoading={isLoading} {...epgProps.getEpgProps()} >
                <Layout
                    {...epgProps.getLayoutProps()}
                    renderProgram={(props) => <ProgramItem {...props} />}
                />
            </Epg>
        </div>
    );
};

export default App;