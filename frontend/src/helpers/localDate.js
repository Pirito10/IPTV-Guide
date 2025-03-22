// Función para obtener la fecha y hora local en formato ISO
export const getLocalDate = () => {
    const now = new Date();
    const offset = now.getTimezoneOffset();
    const localTime = new Date(now.getTime() - offset * 60 * 1000);
    return localTime.toISOString().slice(0, 19);
}