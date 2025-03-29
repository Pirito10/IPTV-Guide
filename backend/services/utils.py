import requests
from datetime import datetime, timedelta
from config import cache, config

# Función para descargar un archivo desde una URL
def fetch_file(url):
    try:
        response = requests.get(url, timeout=config.FILE_TIMEOUT)
        # Lanzamos una excepción si hay un error de estado en la respuesta
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar {url}:\n{e}\n")
        return None

# Función para convertir la fecha y hora de la guía EPG a formato ISO 8601
def convert_epg_time(epg_time):
    try:
        # Extraemos la fecha y zona horaria
        date_part = epg_time[:14]  # "YYYYMMDDHHMMSS"
        tz_offset = epg_time[15:]  # "+0100"

        # Convertimos la fecha a objeto datetime
        dt = datetime.strptime(date_part, "%Y%m%d%H%M%S")

        # Si hay un desfase horario, lo convertimos a UTC
        if tz_offset:
            sign = 1 if tz_offset[0] == "+" else -1
            hours_offset = int(tz_offset[1:3])
            minutes_offset = int(tz_offset[3:5])
            dt -= timedelta(hours=sign * hours_offset, minutes=sign * minutes_offset) # Restamos el desfase para llevarlo a UTC

        return dt.isoformat() + "Z"  # Convertimos a formato ISO 8601
    except Exception as e:
        print(f"Error al convertir fecha EPG: {epg_time}, {e}")
        return None
    
# Función para comprobar si un logo es válido
def get_valid_logo(channel_id, logo_url):
    # Si el logo es accesible, lo devolvemos
    if logo_url and is_url_accessible(logo_url):
        return logo_url

    # Comprobamos si el canal existe en la guía EPG
    if channel_id in cache.cached_epg_data:
        # Obtenemos su logo de la guía EPG
        epg_logo = cache.cached_epg_data[channel_id].get("logo")
        # Si este logo es accesible, lo devolvemos
        if epg_logo and is_url_accessible(epg_logo):
            return epg_logo

    # Si no hay logo válido, no devolvemos ninguna URL
    return None
    
# Función para comprobar si una URL es accesible
def is_url_accessible(url):
    # Enviamos una solicitud HEAD a la URL
    try:
        response = requests.head(url, timeout=config.LOGO_TIMEOUT)
        # Consideramos como respuesta válida un código 200 o 403 (no accesible desde fuera del navegador, pero funcional)
        return response.status_code in (200, 403)
    except requests.exceptions.SSLError:
        # Consideramos los errores de certificado SSL como válidos
        return True
    except requests.RequestException:
        return False