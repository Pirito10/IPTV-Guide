import { ChannelBox, ChannelLogo } from 'planby'
import { FALLBACK_LOGO } from '../helpers/constants'

export const ChannelItem = ({ channel, onClick }) => {
    const { position, uuid, logo } = channel
    return (
        <ChannelBox
            {...position}
            title={uuid} // Tooltip con el nombre del canal
            onClick={onClick} // Mostramos el modal al hacer click
        >
            <ChannelLogo
                src={logo}
                // Ponemos el logo de respaldo si hubo un error al cargar la imagen
                onError={e => e.currentTarget.src = FALLBACK_LOGO}
                // Añadimos un efecto de zoom al pasar el ratón
                onMouseOver={e => e.currentTarget.style.transform = 'scale(1.3)'}
                onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
                style={{
                    transition: 'transform 0.2s',
                    cursor: 'pointer'
                }}
            />
        </ChannelBox>
    )
}