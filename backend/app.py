from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
from routes import routes
from services.updater import update_epg

# Servidor Flask
app = Flask(__name__)
app.register_blueprint(routes)
CORS(app)

# Planificador de tareas
scheduler = BackgroundScheduler()

if __name__ == "__main__":
    try:
        # Actualizamos la guía EPG y la lista M3U
        update_epg(scheduler)

        # Programamos las actualizaciones de la guía EPG
        scheduler.add_job(partial(update_epg, scheduler), "cron", hour="10,14,18,22", minute=0)
        scheduler.start()

        # Iniciamos el servidor Flask
        app.run(host="0.0.0.0")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()