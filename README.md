# IPTV Guide
_IPTV Guide_ is a **web-based electronic program guide viewer** for IPTV channels, providing a fast and user-friendly way to explore TV schedules in real time.

## About The Project

The frontend is built with [React](https://react.dev) and powered by [Planby](https://planby.app), offering a responsive and visually intuitive timeline interface. Users can browse through channels, view current and upcoming programs, filter by group, search by name, and open modals with detailed information or playback options.

The backend, developed with [Flask](https://flask.palletsprojects.com), parses IPTV playlists (M3U) and electronic program guides (XML) to serve up-to-date channel and EPG data. It includes caching, scheduled background updates, local backups, and file-based logging to ensure continuous operation even under network issues.

## How To Run

### Backend

#### Requirements
Make sure you have [Python](https://www.python.org/downloads/) installed on your system. Then install the required dependencies with:

```bash
pip install -r backend/requirements.txt
```

#### Configuration
Open the [config.py](backend/config/config.py) file to adjust settings such as update intervals, URLs, backup locations, logging level, and more.

> [!WARNING]
> If you use the default M3U URL, [ZeroNet]() must be installed and running.

#### Usage
Once the dependencies are installed, you can run the development server with:
```bash
python -m backend.app
```
This will:
- Download and parse the M3U and EPG files
- Launch a local Flask server at `http://localhost:5000`
- Expose three API endpoints:
  - `/api/channels` - returns the parsed channel list
  - `/api/epg` - returns the program guide (EPG)
  - `/api/health` - returns the health status of the server