import { useEffect, useRef } from 'react'
import { FaTimes } from 'react-icons/fa'
import '@styles/Modal.css'

// Componente para mostrar un modal con los grupos para filtrar
export const FilterModal = ({ groups, selectedGroups, onChange, onClose }) => {
    // Listener para la tecla ESC
    useEffect(() => {
        // Creamos una función para manejar el evento "keydown"
        const handleKeyDown = (e) => {
            if (e.key === "Escape") {
                onClose()
            }
        }
        // Añadimos el listener al documento
        document.addEventListener("keydown", handleKeyDown)
        // Eliminamos el listener al cerrar el modal
        return () => document.removeEventListener("keydown", handleKeyDown)
    })

    const modalRef = useRef() // Referencia al modal

    // Listener para clicks
    useEffect(() => {
        // Creamos una función para manejar el evento "mousedown"
        const handleClickOutside = (e) => {
            if (!modalRef.current.contains(e.target)) {
                onClose()
            }
        }
        // Añadimos el listener al documento
        document.addEventListener("mousedown", handleClickOutside)
        // Eliminamos el listener al cerrar el modal
        return () => document.removeEventListener("mousedown", handleClickOutside)
    })

    // Función para cambiar la selección de un grupo
    const toggleGroup = (group) => {
        // Añadimos o eliminamos el grupo de la selección de grupos
        const updatedSelection = selectedGroups.includes(group) ? selectedGroups.filter(g => g !== group) : [...selectedGroups, group]
        // Actualizamos los grupos seleccionados con la nueva selección
        onChange(updatedSelection)
    }

    return (
        <div className="modal" ref={modalRef}>
            <div className="modal-header">
                <h2 className="modal-title">Grupos de canales</h2>
                <button className="modal-close" onClick={onClose}><FaTimes /></button>
            </div>

            <div className="modal-body">
                {groups.map((group) => (
                    <label key={group}>
                        <input
                            type="checkbox"
                            checked={selectedGroups.includes(group)}
                            onChange={() => { toggleGroup(group) }}
                        />
                        {group}
                    </label>
                ))}
            </div>
        </div>
    )
}