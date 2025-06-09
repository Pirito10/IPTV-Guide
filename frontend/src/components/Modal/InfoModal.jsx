import { Modal } from '@components'
import { INFO_MODAL_TEXTS, INFO_MODAL_LINKS } from '@utils/constants'
import '@styles/Modal/InfoModal.css'

// Componente para mostrar un modal con información general
export const InfoModal = ({ onClose }) => {
    // Creamos la cabecera del modal
    const header = (
        <h2 className="modal-title">{INFO_MODAL_TEXTS.TITLE}</h2>
    )

    // Creamos el cuerpo del modal
    const body = (
        <div className="info-modal-content">
            <section className="info-section">
                <h3>ℹ️ ¿Qué es esta aplicación?</h3>
                <p>Esta guía interactiva te permite explorar la programación actual y futura de canales IPTV en tiempo real, con acceso rápido a sus enlaces de reproducción.</p>
                <p>Puedes consultar información más detallada sobre el funcionamiento <a href={INFO_MODAL_LINKS.README} target="_blank">aquí</a>.</p>
            </section>

            <section className="info-section">
                <h3>⚙️ ¿Cómo se usa?</h3>
                <ul>
                    <li>
                        Instala <a href={INFO_MODAL_LINKS.ACESTREAM} target="_blank">Ace Stream</a> en tu dispositivo:
                        <ul>
                            <li><a href={INFO_MODAL_LINKS.ACESTREAM_PC} target="_blank">PC</a></li>
                            <li><a href={INFO_MODAL_LINKS.ACESTREAM_ANDROID} target="_blank">Android</a></li>
                            <li>Android TV</li>
                        </ul>
                    </li>
                    <li>Utiliza la barra superior para buscar canales o filtrarlos por grupo.</li>
                    <li>Haz click en un programa para ver su descripción detallada.</li>
                    <li>Haz click en un canal para ver los enlaces disponibles.</li>
                    <li>Copia el ID para reproducirlo en Ace Stream, o pulsa <b>"Reproducir"</b> para abrirlo directamente.</li>
                </ul>
                <p>Puedes consultar instrucciones de uso más detalladas <a href={INFO_MODAL_LINKS.INSTRUCTIONS} target="_blank">aquí</a>.</p>
            </section>

            <div className="info-footer">
                <div className="info-footer-links">
                    <a href={INFO_MODAL_LINKS.GITHUB} target="_blank">💾 GitHub</a>
                    <a href={INFO_MODAL_LINKS.DONATIONS} target="_blank">💖 Donaciones</a>
                    <a href={INFO_MODAL_LINKS.CHANNELS} target="_blank">📺 Canales</a>
                    <a href={INFO_MODAL_LINKS.EPG} target="_blank">🗓️ Guía TV</a>
                    <a href={INFO_MODAL_LINKS.HELP} target="_blank">🛠️ Ayuda</a>
                    <a href={INFO_MODAL_LINKS.FAQ} target="_blank">❓ FAQ</a>
                </div>
                <div className="info-footer-credits">
                    <span>👨🏻‍💻 Desarrollado por <a href={INFO_MODAL_LINKS.AUTHOR} target="_blank">{INFO_MODAL_TEXTS.AUTHOR}</a></span>
                    <span>🧪 Versión: {__APP_VERSION__}</span>
                </div>
            </div>
        </div>
    )

    return (
        <Modal header={header} body={body} onClose={onClose} />
    )
}