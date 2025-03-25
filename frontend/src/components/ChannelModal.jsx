import { FaRegCopy, FaPlay } from "react-icons/fa";
import "./ChannelModal.css"

export const ChannelModal = ({ channel, onClose }) => {
    return (
        <div className="channel-modal">
            <button className="channel-modal-close" onClick={onClose}>✖</button>

            <div className="channel-modal-header">
                <img
                    src={channel.logo}
                    className="channel-modal-logo"
                />
                <h2 className="channel-modal-title">{channel.uuid}</h2>
            </div>

            {channel.streams?.map((stream, index) => (
                <div key={index} className="channel-stream">
                    <div className="channel-stream-name">{stream.name}</div>
                    <button
                        className="channel-stream-button channel-stream-copy-button"
                        onClick={() => navigator.clipboard.writeText(stream.url)}
                    >
                        <FaRegCopy className="channel-stream-button-icon" />
                        Copiar ID
                    </button>
                    <button
                        className="channel-stream-button channel-stream-play-button"
                        onClick={() => window.open(`acestream://${stream.url}`)}
                    >
                        <FaPlay className="channel-stream-button-icon" />
                        Reproducir
                    </button>
                </div>
            ))}
        </div>
    );
};