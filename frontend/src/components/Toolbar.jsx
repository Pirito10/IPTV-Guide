import React from 'react'
import '@styles/Toolbar.css'

export const Toolbar = () => {
    return (
        <div className="toolbar">
            <button className="toolbar-button">Filtrar</button>
            <input
                type="text"
                className="toolbar-search"
                placeholder="Buscar canales..."
            />
            <button className="toolbar-button">Info</button>
        </div>
    )
}