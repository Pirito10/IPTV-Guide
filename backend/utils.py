import requests
from datetime import datetime, timedelta

# Función para descargar un archivo desde una URL
def fetch_file(url):
    try:
        response = requests.get(url, timeout=10)
        # Lanzamos una excepción si hay un error
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
            delta = timedelta(hours=sign * hours_offset, minutes=sign * minutes_offset)
            dt -= delta  # Restamos el desfase para llevarlo a UTC

        return dt.isoformat() + "Z"  # Convertimos a formato ISO 8601
    except Exception as e:
        print(f"Error al convertir fecha EPG: {epg_time}, {e}")
        return None