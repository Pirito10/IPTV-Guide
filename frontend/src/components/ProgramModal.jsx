import { Modal } from '@components/Modal'
import { FALLBACK_LOGO } from '@utils/constants'
import '@styles/ProgramModal.css'

// Componente para mostrar un modal con la información de un programa
export const ProgramModal = ({ program, logo, onClose }) => {
    // Creamos la cabecera del modal
    const header = (
        <>
            <img
                className="modal-logo"
                src={logo}
                onError={e => e.currentTarget.src = FALLBACK_LOGO}
            />
            <h2 className="modal-title">{program.title}</h2>
        </>
    )

    // Creamos el cuerpo del modal
    const body = (
        <div className="program-modal-description">{program.description}</div>
    )

    return (
        <Modal header={header} body={body} onClose={onClose} />
    )
}