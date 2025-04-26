import { ChannelBox, ChannelLogo } from 'planby'
import { FALLBACK_LOGO } from '@utils/constants'
import '@styles/ChannelItem.css'

export const ChannelItem = ({ channel, onClick }) => {
    const { position, uuid, logo } = channel

    // Función para poner el logo de respaldo
    const handleImageError = e => {
        e.currentTarget.src = FALLBACK_LOGO
    }

    return (
        <ChannelBox
            {...position}
            title={uuid} // Tooltip con el nombre del canal
            onClick={onClick} // Mostramos el modal al hacer click
        >
            <ChannelLogo
                className="channel-logo"
                src={logo}
                onError={handleImageError} // Ponemos el logo de respaldo si hubo un error al cargar la imagen
            />
        </ChannelBox>
    )
}