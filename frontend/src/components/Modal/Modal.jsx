import { useEffect } from 'react'
import { FaTimes } from 'react-icons/fa'
import { MODAL_CLOSE_KEY } from '@utils/constants'
import '@styles/Modal/Modal.css'

// Componente para mostrar un modal genérico
export const Modal = ({ header, body, onClose }) => {
    // Función para cerrar el modal al presionar la tecla "Escape"
    useEffect(() => {
        // Creamos una función para manejar el evento "keydown"
        const handleKeyDown = e => {
            if (e.key === MODAL_CLOSE_KEY) onClose()
        }
        // Añadimos el listener de "keydown" a la ventana
        window.addEventListener('keydown', handleKeyDown)
        // Eliminamos el listener al cerrar el modal
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [])

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal" onClick={e => { e.stopPropagation() }}>
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