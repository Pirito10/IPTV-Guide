import { useEffect } from 'react'
import { FaTimes } from 'react-icons/fa'
import '@styles/Modal.css'

// Componente para mostrar un modal genérico
export const Modal = ({ header, body, onClose }) => {
    // Listener para la tecla ESC
    useEffect(() => {
        // Creamos una función para manejar el evento "keydown"
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') onClose()
        }
        // Añadimos el listener al documento
        window.addEventListener('keydown', handleKeyDown)
        // Eliminamos el listener al cerrar el modal
        return () => window.removeEventListener('keydown', handleKeyDown)
    })

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal" onClick={(e) => { e.stopPropagation() }}>
                <div className="modal-header">
                    <button className="modal-close" onClick={onClose}><FaTimes /></button>
                    {header}
                </div>

                <div className="modal-body">
                    {body}
                </div>
            </div>
        </div>
    )
}