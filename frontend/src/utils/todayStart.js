// Función para obtener la fecha local a las 00:00 en formato ISO 8601
export const getTodayStart = () => {
    // Obtenemos la fecha y hora actual
    const now = new Date()
    // Obtenemos el desfase horario en milisegundos
    const offset = now.getTimezoneOffset() * 60 * 1000
    // Restamos el desfase horario
    const localTime = new Date(now.getTime() - offset)
    // Eliminamos la hora, minutos y segundos
    const dateOnly = localTime.toISOString().slice(0, 10)
    // Devolvemos la fecha con la hora a medianoche
    return `${dateOnly}T00:00:00`
}