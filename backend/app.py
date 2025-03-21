from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
import updater
import routes

# Servidor Flask
app = Flask(__name__)
CORS(app)

app.register_blueprint(routes.routes)

# Planificador de tareas
scheduler = BackgroundScheduler()

# Programamos la actualización de la guía EPG
scheduler.add_job(partial(updater.update_epg, scheduler), "cron", hour="10,14,18,22", minute=0)
scheduler.start()

# Actualizamos la guía EPG y la lista M3U al iniciar la aplicación
updater.update_epg(scheduler)

# Iniciamos el servidor Flask
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()