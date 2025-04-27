import { Modal } from '@components'
import '@styles/Modal/FilterModal.css'

// Componente para mostrar un modal con los grupos para filtrar
export const FilterModal = ({ groups, selectedGroups, onChange, onClose }) => {
    // Función para cambiar la selección de un grupo
    const toggleGroup = (group) => {
        // Añadimos o eliminamos el grupo de la selección de grupos
        const updatedSelection = selectedGroups.includes(group) ? selectedGroups.filter(g => g !== group) : [...selectedGroups, group]
        // Actualizamos los grupos seleccionados con la nueva selección
        onChange(updatedSelection)
    }

    // Creamos la cabecera del modal
    const header = (
        <h2 className="modal-title">Grupos de canales</h2>
    )

    // Creamos el cuerpo del modal, con un selector para cada grupo
    const body = (
        <div className="groups-container">
            {groups.map((group) => (
                <label key={group} className="group">
                    <input
                        type="checkbox"
                        checked={selectedGroups.includes(group)}
                        onChange={() => { toggleGroup(group) }}
                    />
                    {group}
                </label>
            ))}
        </div>
    )

    return (
        <Modal header={header} body={body} onClose={onClose} />
    )
}