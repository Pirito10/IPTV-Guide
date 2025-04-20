import React, { useState } from 'react'
import { FilterModal } from '@components'
import '@styles/Toolbar.css'

// Componente para mostrar la barra de herramientas
export const Toolbar = ({ groups, onGroupChange }) => {
    const [showFilterModal, setShowFilterModal] = useState(false) // Estado para el modal de filtrado

    return (
        <div className="toolbar">
            <button className="toolbar-button" onClick={() => setShowFilterModal(true)}>Filtrar</button>
            <input className="toolbar-search" type="text" placeholder="Buscar canales..." />
            <button className="toolbar-button">Info</button>

            {showFilterModal && <FilterModal onClose={() => setShowFilterModal(false)} />}
        </div>
    )
}