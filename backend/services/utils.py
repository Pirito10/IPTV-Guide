import os
import requests
from datetime import datetime, timedelta
from config import cache, config
from services.logger import logger

# Función para descargar un archivo desde una URL
def fetch_file(url):
    logger.info(f"Downloading content from {url}...")
    try:
        response = requests.get(url, timeout=config.FILE_TIMEOUT)
        # Lanzamos una excepción si hay un error de estado en la respuesta
        response.raise_for_status()
        logger.info(f"Download completed successfully")
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download content: {e}")
        return None


# Función para guardar un contenido en un fichero
def save_file(content, filename):
    logger.info(f"Saving file {filename}...")
    try:
        # Obtenemos la ruta absoluta al directorio de este fichero
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Subimos un nivel y creamos/entramos al directorio destino
        target_dir = os.path.join(base_dir, "..", config.BACKUP_DIRECTORY)
        os.makedirs(target_dir, exist_ok=True)

        # Ruta absoluta al fichero
        path = os.path.abspath(os.path.join(target_dir, filename))

        # Abrimos el fichero y escribimos el contenido
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"File saved successfully to {path}")
    except Exception as e:
        logger.error(f"Failed to save file to {path}: {e}")


# Función para cargar el contenido de un fichero
def load_file(filename):
    logger.info(f"Loading file {filename}...")
    try:
        # Obtenemos la ruta absoluta al directorio de este fichero
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Subimos un nivel y entramos al directorio objetivo
        target_dir = os.path.join(base_dir, "..", config.BACKUP_DIRECTORY)

        # Ruta absoluta al fichero
        path = os.path.abspath(os.path.join(target_dir, filename))

        # Abrimos el fichero y leemos el contenido
        with open(path, "r", encoding="utf-8") as f:
            logger.info(f"File loaded successfully from {path}")
            return f.read()
    except Exception as e:
        logger.error(f"Failed to load file from {path}: {e}")


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
    # Comprobamos si la URL está en la caché
    if url in cache.cached_logos:
        # Comprobamos si ha expirado
        if datetime.now() - cache.cached_logos[url] < timedelta(hours=config.LOGO_TTL):
            return True
        else:
            del cache.cached_logos[url]
        
    # Enviamos una solicitud HEAD a la URL
    try:
        response = requests.head(url, timeout=config.LOGO_TIMEOUT)
        # Consideramos como respuesta válida un código 200 o 403 (no accesible desde fuera del navegador, pero funcional)
        is_valid = response.status_code in (200, 403)
    except requests.exceptions.SSLError:
        # Consideramos los errores de certificado SSL como válidos
        is_valid = True
    except requests.RequestException:
        # Consideramos cualquier otro error como inválido
        is_valid = False

    # Si la URL es válida, la guardamos en caché
    if is_valid:
        cache.cached_logos[url] = datetime.now()

    return is_valid