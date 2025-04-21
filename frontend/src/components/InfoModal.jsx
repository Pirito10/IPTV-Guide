import { Modal } from '@components/Modal'
import '@styles/Modal.css'

// Componente para mostrar un modal con información general
export const InfoModal = ({ onClose }) => {
    // Creamos la cabecera del modal
    const header = (
        <h2 className="modal-title">Información</h2>
    )

    // Creamos el cuerpo del modal
    const body = (
        <></>
    )

    return (
        <Modal header={header} body={body} onClose={onClose} />
    )
}