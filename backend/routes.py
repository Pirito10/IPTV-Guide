import threading
from flask import jsonify, Blueprint

from backend.config import cache
from backend.services.logger import logger
from backend.services.updater import update_m3u

routes = Blueprint("routes", __name__)

m3u_lock = threading.Lock()

# Ruta a la API para obtener los canales
@routes.route("/api/channels")
def channels():
    logger.info("Request to /api/channels received")

    # Intentamos actualizar la lista M3U en exclusión mutua
    with m3u_lock:
        try:
            update_m3u()
        except Exception as e:
            logger.error(f"Unexpected error while updating M3U list: {e}")

    # Si no hay datos de canales, devolvemos un error
    if not cache.cached_m3u_data:
        return jsonify({"error": "No channels available"}), 503

    # Devolvemos la lista de canales almacenada en caché
    return jsonify(cache.cached_m3u_data)


# Ruta a la API para obtener la guía EPG
@routes.route("/api/epg")
def epg():
    logger.info("Request to /api/epg received")

    # Si no hay guía EPG, devolvemos un error
    if not cache.cached_epg_data:
        return jsonify({"error": "No EPG available"}), 503

    # Devolvemos la guía almacenada en caché
    return jsonify(cache.cached_epg_data)


# Ruta a la API para comprobar el estado del servicio
@routes.route("/api/health")
def health_check():
    # Comprobamos el estado de la lista M3U y la guía EPG
    m3u_ok = bool(cache.cached_m3u_data)
    epg_ok = bool(cache.cached_epg_data)

    # Si no hay datos en alguna de las dos, devolvemos un error
    if not (m3u_ok and epg_ok):
        logger.error("Health check failed, M3U or EPG data is missing")
        return jsonify({
            "status": "degraded",
            "m3u_data": m3u_ok,
            "epg_data": epg_ok
        }), 503
    
    # Si hay datos en ambas, devolvemos un estado OK
    return jsonify({
        "status": "ok"
    }), 200