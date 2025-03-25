import { ChannelBox, ChannelLogo } from 'planby';

export const ChannelItem = ({ channel, onClick }) => {
    const { position, logo } = channel;
    return (
        <ChannelBox
            {...position}
            title={channel.name} // Tooltip con el nombre del canal
            onClick={onClick} // Mostramos el modal al hacer click
        >
            <ChannelLogo
                src={logo}
                // Añadimos un efecto de zoom al pasar el ratón
                onMouseOver={(e) => (e.currentTarget.style.transform = 'scale(1.3)')}
                onMouseOut={(e) => (e.currentTarget.style.transform = 'scale(1)')}
                style={{
                    transition: 'transform 0.2s',
                    cursor: 'pointer'
                }}
            />
        </ChannelBox>
    );
};