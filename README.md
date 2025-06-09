# IPTV Guide
_IPTV Guide_ is a **web-based electronic program guide viewer** for IPTV channels, providing a fast and user-friendly way to explore TV schedules in real time.

## About The Project

This project is a self-hosted solution for browsing IPTV channels and their schedules in real time through a modern web interface.

The frontend is built with [React](https://react.dev) and powered by [Planby](https://planby.app). It provides a fast and responsive interface where users can scroll through channels, view current and upcoming programs, filter by group, search by keywords, and open modals with detailed information or playback options.

The backend, implemented with [Flask](https://flask.palletsprojects.com), is responsible for fetching, parsing and serving IPTV data. It supports M3U playlists and XML electronic program guides, transforming them into a consistend format for the frontend. It also includes caching, automatic scheduled updates, local backups as fallback, and file-based logging to ensure robustness and availability, even under unstable network conditions.

> [!NOTE]
> While the system is minimally customizable, it is designed to run autonomously on a server, avoiding the need for manual downloads or additional tools on the client side.

## How To Run

> [!TIP]
> See [Production Notes](#production-notes) for guidance on deploying the app in a production environment.

### Backend
#### Requirements
Make sure [Python](https://www.python.org/downloads) is installed on your system. Then install the required dependencies with:

```bash
pip install -r backend/requirements.txt
```

#### Configuration
Open the [`backend/config/config.py`](backend/config/config.py) file to adjust settings such as update intervals, source URLs, backup locations, logging level, and more.

> [!WARNING]
> If you use the default M3U URL, [ZeroNet](https://zeronet.io) must be installed and running.

#### Usage
Once the dependencies are installed, run the backend with:
```bash
python -m backend.app
```
The server will be available at `http://localhost:5000`, exposing the following API endpoints:
- `/api/channels` — returns the parsed IPTV channel list.
- `/api/epg` — returns the parsed electronic program guide.
- `/api/health` — returns a basic health check of the server.

### Frontend
#### Requirements
Make sure [Node.js](https://nodejs.org/en/download) is installed on your system. Then install the required dependencies with:
```bash
cd frontend
npm install
```

#### Configuration
Open the [`frontend/src/utils/constants.js`](frontend/src/utils/constants.js) file to adjust API URLs to match your backend server.

> [!WARNING]
> If you use the default settings, the frontend will try to connect to the public backend server hosted by the author at `https://api.tebas-ladron.me`. This endpoint is not guaranteed to remain available and may be removed or changed at any time.

#### Build
Once the dependencies are installed, build the frontend with:
```bash
npm run build
```

#### Usage
Once the build is finished, run the frontend server with:
```bash
npm run preview
```
The app will be available at `http://localhost:5173`.

## About the Code

This project is divided into two main parts: the **backend**, responsible for data processing and API serving; and the **frontend**, responsible for rendering the guide and handling user interaction.

### Backend

The backend is built with Flask and performs the following tasks:
- <u>Data fetching</u>: downloads the IPTV playlist and program guide from configurable URLs.
- <u>Parsing and transformation</u>: parses raw data into a structured format, groups streams by channel, validates logos, filters program entries, and more.
- <u>Caching and backups</u>: stores the latest valid data in memory and saves local backups to disk to ensure resilience against network or source failures.
- <u>Scheduled updates</u>: runs periodic tasks to refresh the playlist and EPG in the background, ensuring the data is always up-to-date.
- <u>Logging</u>: records events and errors into timestamped log files for easy debugging and monitoring.
- <u>API serving</u>: exposes endpoints to retrieve channel and EPG data in JSON format for the frontend to consume.

> [!NOTE]
> The backend is designed to be moderately customizable through the configuration file, allowing users to adapt it to their needs. It runs independently from the frontend and can be deployed almost anywhere.

### Frontend

The frontend is a single-page application built with React and Planby, designed to render the IPTV guide as a timeline-based interface. It offers the following features:
- <u>Channel browsing</u>: scrollable view of all available IPTV channels.
- <u>Timeline-based EPG</u>: visual layout of programs over time, with support for horizontal scrolling and current-time tracking.
- <u>Modals for channels and programs</u>: clickable elements open overlays with detailed information or playback options.
- <u>Filtering and search</u>: filter channels by group or search by keywords across channel names, program titles, and descriptions.
- <u>Responsive UI</u>: optimized for both desktop and mobile use.

> [!NOTE]
> The frontend is built to be lightweight and fast, considering the large amount of data it handles. All content is rendered dynamically at runtime using the backend API.

> [!WARNING]
> Some UI features are limited by the capabilities of the Planby free tier, such as support for only a single day of schedule data.

## Production Notes

This project is designed to be self-hosted and can be deployed in production with various configurations, depending on your environment and needs.

A typical production setup might include:
- Running the backend with a production WSGI server such as [Gunicorn](https://gunicorn.org).
- Serving the frontend as static files via [GitHub Pages](https://pages.github.com), [NGINX](https://nginx.org), or similar.
- Using [ZeroNet](https://zeronet.io) to access private or decentralized IPTV playlists, if needed.
- Setting up a reverse proxy to handle requests and serve both frontend and backend seamlessly.
- Setting up HTTPS with [Let's Encrypt](https://letsencrypt.org), especially when frontend and backend are served from different origins.
- Configuring a process manager like [systemd]() to ensure the servers are always running and restarted on failure.

> [!NOTE]
> The application was tested and worked on a low specification machine (Raspberry Pi Zero W). This may vary depending on the amount of data managed and the number of concurrent users.