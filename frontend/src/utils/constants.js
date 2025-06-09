// URLs a los endpoints del backend
export const CHANNELS_URL = "https://api.tebas-ladron.me/api/channels"
export const EPG_URL = "https://api.tebas-ladron.me/api/epg"

// Valores por defecto para los parámetros de los canales
export const FALLBACK_LOGO = "https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM="
export const DEFAULT_GROUP = "OTROS"

// Tiempo de espera para procesar la búsqueda de canales
export const SEARCH_DEBOUNCE_DELAY = 500
// Duración de la animación de filtrado
export const FILTER_ANIMATION_DURATION = 300

// Umbral de coincidencia para la búsqueda con Fuse.js
export const FUSE_SEARCH_THRESHOLD = 0.4

// Ancho de la guía EPG en píxeles
export const EPG_DAY_WIDTH = 10000