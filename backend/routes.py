from flask import jsonify, Blueprint
from services.logger import logger
from services.updater import update_m3u
from config import cache

routes = Blueprint("routes", __name__)

# Ruta a la API para obtener los canales
@routes.route("/api/channels")
def channels():
    logger.info("Request to /api/channels received")

    # Intentamos actualizar la lista M3U
    try:
        update_m3u()
    except Exception as e:
        logger.error(f"Unexpected error while updating M3U list: {e}")

    # Si no hay datos de canales, devolvemos un error
    if not cache.cached_m3u_data:
        return jsonify({"error": "No channels available"}), 500

    # Devolvemos la lista de canales almacenada en caché
    return jsonify(cache.cached_m3u_data)


# Ruta a la API para obtener la guía EPG
@routes.route("/api/epg")
def epg():
    logger.info("Request to /api/epg received")

    # Si no hay guía EPG, devolvemos un error
    if not cache.cached_epg_data:
        return jsonify({"error": "No EPG available"}), 500

    # Devolvemos la guía almacenada en caché
    return jsonify(cache.cached_epg_data)