import { FaRegCopy, FaPlay } from 'react-icons/fa'
import { Modal } from '@components'
import { FALLBACK_LOGO } from '@utils/constants'
import '@styles/Modal/ChannelModal.css'

// Componente para mostrar un modal con los streams de un canal
export const ChannelModal = ({ channel, onClose }) => {
    // Creamos la cabecera del modal
    const header = (
        <>
            <img
                className="modal-logo"
                src={channel.logo}
                onError={e => e.currentTarget.src = FALLBACK_LOGO}
            />
            <h2 className="modal-title">{channel.uuid}</h2>
        </>
    )

    // Creamos el cuerpo del modal
    const body = (
        <>
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
        </>
    )

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
        <Modal header={header} body={body} onClose={onClose} />
    )
}