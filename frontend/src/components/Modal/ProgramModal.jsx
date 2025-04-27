import { Modal } from '@components'
import { FALLBACK_LOGO } from '@utils/constants'
import '@styles/Modal/ProgramModal.css'

// Componente para mostrar un modal con la información de un programa
export const ProgramModal = ({ program, logo, onClose }) => {
    // Función para poner el logo de respaldo
    const handleImageError = e => {
        e.currentTarget.src = FALLBACK_LOGO
    }

    // Creamos la cabecera del modal, con el logo del canal y el nombre del programa 
    const header = (
        <>
            <img
                className="modal-logo"
                src={logo}
                onError={handleImageError}
            />
            <h2 className="modal-title">{program.title}</h2>
        </>
    )

    // Creamos el cuerpo del modal, con la descripción del programa
    const body = (
        <div className="program-modal-description">{program.description}</div>
    )

    return (
        <Modal header={header} body={body} onClose={onClose} />
    )
}