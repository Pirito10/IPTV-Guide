import { ChannelBox, ChannelLogo } from 'planby'
import { FALLBACK_LOGO } from '@helpers/constants'
import '@styles/ChannelItem.css'

export const ChannelItem = ({ channel, onClick }) => {
    const { position, uuid, logo } = channel
    return (
        <ChannelBox
            {...position}
            title={uuid} // Tooltip con el nombre del canal
            onClick={onClick} // Mostramos el modal al hacer click
        >
            <ChannelLogo
                className="channel-logo"
                src={logo}
                // Ponemos el logo de respaldo si hubo un error al cargar la imagen
                onError={e => e.currentTarget.src = FALLBACK_LOGO}
            />
        </ChannelBox>
    )
}