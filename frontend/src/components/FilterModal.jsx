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

    return (
        <div className="modal" ref={modalRef}>
            <div className="modal-header">
                <button className="modal-close" onClick={onClose}><FaTimes /></button>
            </div>

            <div className="modal-body">

            </div>
        </div>
    )
}
