export const ChannelModal = ({ channel, onClose }) => {
    return (
        <div style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            backgroundColor: '#1A202C',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 0 10px rgba(0,0,0,0.5)',
            zIndex: 1000,
            color: 'white',
            minWidth: '250px',
            textAlign: 'center'
        }}>
            <h2>{channel.name}</h2>
            <img
                src={channel.logo}
                alt={`Logo de ${channel.name}`}
                style={{ maxWidth: '100px', margin: '10px 0' }}
            />
            <p><strong>ID:</strong> {channel.uuid}</p>
            <button
                onClick={onClose}
                style={{
                    marginTop: '10px',
                    backgroundColor: '#2C7A7B',
                    color: 'white',
                    border: 'none',
                    padding: '6px 12px',
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}
            >
                Cerrar
            </button>
        </div>
    );
};