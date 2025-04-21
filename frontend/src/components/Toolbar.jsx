import React, { useState } from 'react'
import { FaFilter } from 'react-icons/fa'
import { FilterModal, InfoModal } from '@components'
import '@styles/Toolbar.css'

// Componente para mostrar la barra de herramientas
export const Toolbar = ({ groups, selectedGroups, onGroupChange }) => {
    const [showFilterModal, setShowFilterModal] = useState(false) // Estado para el modal de filtrado
    const [showInfoModal, setShowInfoModal] = useState(false) // Estado para el modal de información

    return (
        <div className="toolbar">
            <button className="toolbar-button" onClick={() => setShowFilterModal(true)}>
                <FaFilter className="toolbar-button-icon" />
                Filtrar
            </button>
            <input className="toolbar-search" type="text" placeholder="Buscar canales..." />
            <button className="toolbar-button" onClick={() => setShowInfoModal(true)}>
                Info
            </button>

            {showFilterModal && <FilterModal groups={groups} selectedGroups={selectedGroups} onChange={onGroupChange} onClose={() => setShowFilterModal(false)} />}
            {showInfoModal && <InfoModal onClose={() => setShowInfoModal(false)} />}
        </div>
    )
}