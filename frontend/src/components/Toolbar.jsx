import React, { useState } from 'react'
import { FaFilter } from 'react-icons/fa'
import { FilterModal } from '@components'
import '@styles/Toolbar.css'

// Componente para mostrar la barra de herramientas
export const Toolbar = ({ groups, selectedGroups, onGroupChange }) => {
    const [showFilterModal, setShowFilterModal] = useState(false) // Estado para el modal de filtrado

    return (
        <div className="toolbar">
            <button className="toolbar-button" onClick={() => setShowFilterModal(true)}>
                <FaFilter className="toolbar-button-icon" />
                Filtrar
            </button>
            <input className="toolbar-search" type="text" placeholder="Buscar canales..." />
            <button className="toolbar-button">Info</button>

            {showFilterModal && <FilterModal groups={groups} selectedGroups={selectedGroups} onChange={onGroupChange} onClose={() => setShowFilterModal(false)} />}
        </div>
    )
}