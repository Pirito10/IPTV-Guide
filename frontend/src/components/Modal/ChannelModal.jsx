import { FaRegCopy, FaPlay } from 'react-icons/fa'
import { Modal } from '@components'
import { FALLBACK_LOGO } from '@utils/constants'
import '@styles/Modal/ChannelModal.css'

// Componente para mostrar un modal con los streams de un canal
export const ChannelModal = ({ channel, onClose }) => {
    // Función para poner el logo de respaldo
    const handleImageError = e => {
        e.currentTarget.src = FALLBACK_LOGO
    }

    // Función para copiar un ID de un stream
    const handleCopy = url => {
        navigator.clipboard.writeText(url)
        showCopiedToast()
    }

    // Función para reproducir un stream
    const handlePlay = url => {
        window.open(`acestream://${url}`)
    }

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

    // Creamos la cabecera del modal, con el logo y nombre del canal
    const header = (
        <>
            <img
                className="modal-logo"
                src={channel.logo}
                onError={handleImageError}
            />
            <h2 className="modal-title">{channel.uuid}</h2>
        </>
    )

    // Creamos el cuerpo del modal, con una entrada para cada stream con el nombre, botón para copiar ID y botón para reproducir
    const body = (
        <>
            {channel.streams?.map((stream, index) => (
                <div key={index} className="channel-stream">
                    <div className="channel-stream-name">{stream.name}</div>
                    <button
                        className="channel-stream-button channel-stream-copy-button"
                        onClick={() => handleCopy(stream.url)}
                    >
                        <FaRegCopy className="channel-stream-button-icon" />
                        Copiar ID
                    </button>
                    <button
                        className="channel-stream-button channel-stream-play-button"
                        onClick={() => handlePlay(stream.url)}
                    >
                        <FaPlay className="channel-stream-button-icon" />
                        Reproducir
                    </button>
                </div>
            ))}
        </>
    )

    return (
        <Modal header={header} body={body} onClose={onClose} />
    )
}