import { ChannelBox, ChannelLogo } from 'planby';

export const ChannelItem = ({ channel }) => {
    const { position, logo } = channel;
    return (
        <ChannelBox {...position}>
            <ChannelLogo
                src={logo}
                title={channel.name}
                // Añadimos un efecto de zoom al pasar el ratón
                style={{
                    transition: 'transform 0.2s ease'
                }}
                onMouseOver={(e) => (e.currentTarget.style.transform = 'scale(1.3)')}
                onMouseOut={(e) => (e.currentTarget.style.transform = 'scale(1)')}
            />
        </ChannelBox>
    );
};

//  TODO manejar errores para imagen de respaldo