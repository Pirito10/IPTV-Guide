import { useEffect, useRef } from "react"
import { FaRegCopy, FaPlay, FaTimes } from "react-icons/fa";
import { FALLBACK_LOGO } from '../helpers/constants';
import "./ChannelModal.css"

// Componente para mostrar un modal con los streams de un canal
export const ChannelModal = ({ channel, onClose }) => {
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

    const modalRef = useRef(); // Referencia al modal

    // Listener para clicks
    useEffect(() => {
        // Creamos una función para manejar el evento "mousedown"
        const handleClickOutside = (e) => {
            if (!modalRef.current.contains(e.target)) {
                onClose();
            }
        };
        // Añadimos el listener al documento
        document.addEventListener("mousedown", handleClickOutside);
        // Eliminamos el listener al cerrar el modal
        return () => document.removeEventListener("mousedown", handleClickOutside);
    });

    return (
        <div className="channel-modal" ref={modalRef}>
            <button className="channel-modal-close" onClick={onClose}><FaTimes /></button>

            <div className="channel-modal-header">
                <img
                    className="channel-modal-logo"
                    src={channel.logo}
                    onError={e => e.currentTarget.src = FALLBACK_LOGO}
                />
                <h2 className="channel-modal-title">{channel.uuid}</h2>
            </div>

            {channel.streams?.map((stream, index) => (
                <div key={index} className="channel-stream">
                    <div className="channel-stream-name">{stream.name}</div>
                    <button
                        className="channel-stream-button channel-stream-copy-button"
                        onClick={() => navigator.clipboard.writeText(stream.url)}
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
    );
};