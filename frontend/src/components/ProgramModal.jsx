import { useEffect, useRef } from "react"
import { FaTimes } from "react-icons/fa"
import { FALLBACK_LOGO } from '@utils/constants'
import "@styles/Modal.css"
import "@styles/ProgramModal.css"

export const ProgramModal = ({ program, logo, onClose }) => {
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
                <img
                    className="modal-logo"
                    src={logo}
                    onError={e => e.currentTarget.src = FALLBACK_LOGO}
                />
                <h2 className="modal-title">{program.title}</h2>
                <button className="modal-close" onClick={onClose}><FaTimes /></button>
            </div>

            <div className="modal-body">
                <div className="program-modal-description">{program.description}</div>
            </div>
        </div>
    )
}
