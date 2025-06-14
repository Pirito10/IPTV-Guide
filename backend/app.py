from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from backend.routes import routes
from backend.config import config
from backend.services.logger import logger
from backend.services.updater import update_m3u, update_epg

logger.info("Starting IPTV-Guide server...")

# Servidor Flask
app = Flask(__name__)
app.register_blueprint(routes, url_prefix=config.API_BASE_PATH)
CORS(app)

# Planificador de tareas
scheduler = BackgroundScheduler()

# Actualizamos la guía EPG y la lista M3U
try:
    logger.info("Running initial M3U list and EPG update...")
    update_m3u(first_run=True)
    update_epg(scheduler, first_run=True)
except Exception as e:
    logger.critical(f"Unexpected error during initial data loading: {e}")

# Programamos las actualizaciones de la guía EPG
scheduler.add_job(lambda: (update_m3u(force=True), update_epg(scheduler)), "cron", hour=config.EPG_SCHEDULER_HOURS, minute=0)
scheduler.start()
logger.info(f"EPG update scheduled at hours: {config.EPG_SCHEDULER_HOURS}")

logger.info("Server started successfully")

# Iniciamos el servidor de desarrollo de Flask
if __name__ == "__main__":
    app.run(config.SERVER_IP, config.SERVER_PORT)