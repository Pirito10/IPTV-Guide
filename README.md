# IPTV Guide
_IPTV Guide_ is a **web-based electronic program guide viewer** for IPTV channels, providing a fast and user-friendly way to explore TV schedules in real time.

## About The Project

This project is a self-hosted solution for browsing IPTV channels and their schedules in real time through a modern web interface.

The frontend is built with [React](https://react.dev) and powered by [Planby](https://planby.app). It provides a fast and responsive interface where users can scroll through channels, view current and upcoming programs, filter by group, search by keywords, and open modals with detailed information or playback options.

The backend, implemented with [Flask](https://flask.palletsprojects.com), is responsible for fetching, parsing and serving IPTV data. It supports M3U playlists and XML electronic program guides, transforming them into a consistend format for the frontend. It also includes caching, automatic scheduled updates, local backups as fallback, and file-based logging to ensure robustness and availability, even under unstable network conditions.

> [!NOTE]
> While the system is minimally customizable, it is designed to run autonomously on a server, avoiding the need for manual downloads or additional tools on the client side.

## How To Run

### Backend

> [!NOTE]
> Go to *production notes* for more information about running the application in production.

#### Requirements
Make sure you have [Python](https://www.python.org/downloads) installed on your system. Then install the required dependencies with:

```bash
pip install -r backend/requirements.txt
```

#### Configuration
Open the [config.py](backend/config/config.py) file to adjust settings such as update intervals, URLs, backup locations, logging level, and more.

> [!WARNING]
> If you use the default M3U URL, [ZeroNet](https://zeronet.io) must be installed and running.

#### Usage
Once the dependencies are installed, you can run the server with:
```bash
python -m backend.app
```
This will expose three API endpoints at `http://localhost:5000`:
- `/api/channels` — returns the parsed IPTV channel list.
- `/api/epg` — returns the parsed electronic program guide.
- `/api/health` — returns a basic health check of the server.

### Frontend

> [!NOTE]
> Go to *production notes* for more information about running the application in production.

#### Requirements
Make sure you have [NodeJS](https://nodejs.org/en/download) installed on your system. Then install the required dependencies with:
```bash
cd frontend
npm install
```

#### Build
Once the dependencies are installed, you can build the frontend with:
```bash
npm run build
```

#### Usage
Once the build is finished, you can run the server with:
```bash
npm run preview
```
Then, open your web browser and navigate to `http://localhost:5173`.

## About the Code

This project is split into two main parts: the **backend**, resposible for data processing and API serving, and the **frontend**, responsible for rendering the guide and handling user interaction.

### Backend

The backend is built with Flask and handles the following tasks:
- Download and parse IPTV data: fetches the M3U playlist and XML program guide from configured URLs, and parses them into structures data.
- Data transformation: groups streams by channel, validates logos, and filters EPG content.
- Caching and backups: stores the latest valid data in memory and writes backups to disk to ensure data persistence in case of URL failures.
- Scheduled updates: runs periodic tasks to refresh data in the background, ensuring the guide is always up-to-date.
- Logging: logs all events and errors into timestamped files for easy debbugging and monitoring.
- API serving: exposes endpoints to retrieve channel and EPG data in JSON format for the frontend to consume.

The backend is designed to be moderately customizable through the configuration file, allowing users to adjust the server to their needs. It runs independently from the frontend, and can be deployed almost anywhere.

### Frontend

The frontend is a single-page application built with React and Plany, designed to display the IPTV program guide in a timeline format. It provides:
- Channel browsing: scrollable view of all available IPTV channels.
- Timeline-based EPG: visual display of programs by time slot, with zoom and scroll support.
- Program & channel modals: click to view detailed information or stream playback options.
- Filtering and search: filter by group or search by words.
- Responsive UI: works on desktop and mobile browsers.

The frontend is built to be lightweight and fast, considering the larga amount of data it handles. Some features are limited due to the customizability of the Planby free tier. It consumes the backend API, rendering all content dynamically at runtime.

## Production Notes

This project is designed to be self-hosted and can be deployed in production with various configurations, depending on your environment and needs.

A typical production setup might include:
- Running the backend with a production WSGI server such as [Gunicorn]().
- Serving the frontend as static files via [GitHub Pages](), [Nginx](), or similar.
- Using [ZeroNet]() to access private or decentralized IPTV playlists, if needed.
- Setting up a reverse proxy to handle requests and serve both frontend and backend seamlessly.
- Setting up HTTPS with [Let's Encrypt](), specially when frontend and backend are served from different origins.
- Configuring a process manager like [systemd]() to ensure the servers are always running and restarted on failure.

> [!NOTE]
> The application was tested and worked on a low specification machine (Raspberry Pi Zero W). This may vary depending on the amount of data managed and the number of concurrent users.