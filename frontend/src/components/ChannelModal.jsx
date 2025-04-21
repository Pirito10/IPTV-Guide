import { useEffect } from 'react'
import { FaTimes, FaRegCopy, FaPlay } from 'react-icons/fa'
import { FALLBACK_LOGO } from '@utils/constants'
import '@styles/Modal.css'
import '@styles/ChannelModal.css'

// Componente para mostrar un modal con los streams de un canal
export const ChannelModal = ({ channel, onClose }) => {
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

    // Función para mostrar el toast de ID copiado
    const showCopiedToast = () => {
        // Creamos el elemento del toast
        const toast = document.createElement("div")
        toast.className = "copied-toast"
        toast.textContent = "ID copiado al portapapeles"
        document.body.appendChild(toast)

        // Iniciamos un temporizador para desvanecer el toast
        setTimeout(() => {
            toast.classList.add("copied-toast-fade-out")
        }, 1000)

        // Iniciamos un temporizador para eliminar el toast
        setTimeout(() => {
            toast.remove()
        }, 2000)
    }

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal" onClick={(e) => { e.stopPropagation() }}>
                <div className="modal-header">
                    <img
                        className="modal-logo"
                        src={channel.logo}
                        onError={e => e.currentTarget.src = FALLBACK_LOGO}
                    />
                    <h2 className="modal-title">{channel.uuid}</h2>
                    <button className="modal-close" onClick={onClose}><FaTimes /></button>
                </div>

                <div className="modal-body">
                    {channel.streams?.map((stream, index) => (
                        <div key={index} className="channel-stream">
                            <div className="channel-stream-name">{stream.name}</div>
                            <button
                                className="channel-stream-button channel-stream-copy-button"
                                onClick={() => {
                                    navigator.clipboard.writeText(stream.url)
                                    showCopiedToast()
                                }}
                            >
                                <FaRegCopy className="channel-stream-button-icon" />
                                Copiar ID
                            </button>
                            <button
                                className="channel-stream-button channel-stream-play-button"
                                onClick={() => window.open(`acestream://${stream.url}`)}
                            >
                                <FaPlay className="channel-stream-button-icon" />
                                Reproducir
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}