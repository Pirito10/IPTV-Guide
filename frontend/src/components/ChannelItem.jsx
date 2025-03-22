import { ChannelBox, ChannelLogo } from 'planby';

export const ChannelItem = ({ channel }) => {
    const { position, logo } = channel;
    return (
        <ChannelBox {...position}>
            <ChannelLogo
                src={logo}
            />
        </ChannelBox>
    );
};