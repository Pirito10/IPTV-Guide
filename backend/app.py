from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from routes import routes
from services.updater import update_m3u, update_epg
from config import config

# Servidor Flask
app = Flask(__name__)
app.register_blueprint(routes)
CORS(app)

# Planificador de tareas
scheduler = BackgroundScheduler()

if __name__ == "__main__":
    try:
        # Actualizamos la guía EPG y la lista M3U
        update_m3u(first_run=True)
        update_epg(scheduler, first_run=True)

        # Programamos las actualizaciones de la guía EPG
        scheduler.add_job(lambda: (update_m3u(force=True), update_epg(scheduler)), "cron", hour=config.EPG_SCHEDULER_HOURS, minute=0)
        scheduler.start()

        # Iniciamos el servidor Flask
        app.run(config.SERVER_IP)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()