// =========================
// 🛰️ Endpoints del backend
// =========================

export const CHANNELS_URL = "https://api.tebas-ladron.me/api/channels"
export const EPG_URL = "https://api.tebas-ladron.me/api/epg"


// ========================
// ⚙️ Parámetros generales
// ========================

export const SEARCH_DEBOUNCE_DELAY = 500 // Tiempo de espera (en milisegundos) antes de procesar la búsqueda
export const FILTER_ANIMATION_DURATION = 300 // Duración (en milisegundos) de la animación de filtrado
export const FUSE_SEARCH_THRESHOLD = 0.4 // Umbral de coincidencia para la búsqueda difusa
export const EPG_DAY_WIDTH = 10000 // Ancho total de la interfaz
export const MODAL_CLOSE_KEY = "Escape" // Tecla para cerrar modales
export const STREAM_PROTOCOL = "acestream://" // Protocolo para abrir streams


// =======================
// 🖼️ Valores por defecto
// =======================

export const FALLBACK_LOGO = "https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM="
export const DEFAULT_GROUP = "OTROS"


// =======================
// 🔔 Animación del toast
// =======================

export const TOAST_FADE_DURATION = 1000 // Tiempo (en milisegundos) hasta comenzar a desvanecer
export const TOAST_REMOVE_DELAY = 2000 // Tiempo (en milisegundos) hasta eliminar el toast


// ====================
// 🧭 Textos y enlaces
// ====================

// Textos de la barra de herramientas
export const TOOLBAR_TEXTS = {
    FILTER: "Filtrar",
    SEARCH_PLACEHOLDER: "Buscar canales...",
    INFO: "Info"
}

// Textos del modal de canales
export const CHANNEL_MODAL_TEXTS = {
    COPY_ID: "Copiar ID",
    PLAY: "Reproducir",
    TOAST_COPY_SUCCESS: "ID copiado al portapapeles"
}

// Textos del modal de filtrado
export const FILTER_MODAL_TEXTS = {
    TITLE: "Grupos de canales"
}

// Textos del modal de información
export const INFO_MODAL_TEXTS = {
    TITLE: "Información",
    AUTHOR: "Pirito10"
}

// Enlaces del modal de información
export const INFO_MODAL_LINKS = {
    README: "TODO",
    ACESTREAM: "https://www.acestream.org",
    ACESTREAM_PC: "https://www.acestream.org/?page=products",
    ACESTREAM_ANDROID: "https://play.google.com/store/apps/details?id=org.acestream.node",
    INSTRUCTIONS: "TODO",
    GITHUB: "https://github.com/Pirito10/IPTV-Guide",
    DONATIONS: "https://paypal.me/Pirito10",
    CHANNELS: "https://ipfs.io/ipns/elcano.top",
    EPG: "https://github.com/davidmuma",
    HELP: "https://github.com/Pirito10/IPTV-Guide/issues/new/choose",
    FAQ: "TODO",
    AUTHOR: "https://github.com/Pirito10"
}