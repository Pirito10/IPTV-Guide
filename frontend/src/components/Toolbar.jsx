import { useState } from 'react'
import { FaFilter, FaInfoCircle } from 'react-icons/fa'
import { FilterModal, InfoModal } from '@components'
import '@styles/Toolbar.css'

// Componente para mostrar la barra de herramientas
export const Toolbar = ({ groups, selectedGroups, onGroupChange, searchInput, onSearchInputChange }) => {
    const [showFilterModal, setShowFilterModal] = useState(false) // Estado para el modal de filtrado
    const [showInfoModal, setShowInfoModal] = useState(false) // Estado para el modal de información

    // Funciones para abrir y cerrar los modales
    const openFilterModal = () => setShowFilterModal(true)
    const closeFilterModal = () => setShowFilterModal(false)
    const openInfoModal = () => setShowInfoModal(true)
    const closeInfoModal = () => setShowInfoModal(false)

    return (
        <div className="toolbar">
            <button className="toolbar-button" onClick={openFilterModal}>
                <FaFilter className="toolbar-button-icon" />
                Filtrar
            </button>
            <input
                className="toolbar-search"
                type="text"
                placeholder="Buscar canales..."
                value={searchInput}
                onChange={e => onSearchInputChange(e.target.value)}
            />
            <button className="toolbar-button" onClick={openInfoModal}>
                <FaInfoCircle className="toolbar-button-icon" />
                Info
            </button>

            {showFilterModal && <FilterModal
                groups={groups}
                selectedGroups={selectedGroups}
                onChange={onGroupChange}
                onClose={closeFilterModal}
            />}
            {showInfoModal && <InfoModal onClose={closeInfoModal} />}
        </div>
    )
}