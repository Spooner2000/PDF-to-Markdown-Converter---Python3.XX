# Admin Automation Dashboard Pro

Umfangreiches Referenzprojekt für ein modular erweiterbares Administrations-Dashboard mit FastAPI-Backend und Electron/React-Frontend. Die Anwendung orientiert sich an der Ausschreibung "Admin Automation Dashboard Pro" und liefert eine vollständig lauffähige Grundlage inklusive Echtzeit-Streaming, RBAC, Demo-Daten und einer modernen UI.

## Projektüberblick

* **Backend:** FastAPI 0.111 mit In-Memory-Datenhaltung, Event-Bus, RBAC (Rollen `administrator`, `operator`, `developer`, `viewer`), WebSocket-Streaming und Hintergrund-Telemetrie.
* **Frontend:** Electron-Shell mit Vite + React, Mantine UI-Bibliothek, Zustand-Store, Echtzeit-Updates über WebSocket und Dashboard-Widgets.
* **Funktionalität:**
  * CRUD-Endpunkte für Routinen, Skripte, Geräte, API-Definitionen, HTTP-Server und virtuelle Umgebungen.
  * Authentifizierung via Token, Benutzerverwaltung und Sitzungsübersicht.
  * Dashboard-Zusammenfassung mit Kennzahlen, Logs, Benachrichtigungen und Live-Event-Stream.
  * Telemetrie-Worker, der Metriken, Logs und Notifications simuliert.

## Verzeichnisstruktur

```
.
├── backend
│   ├── app
│   │   ├── api            # API-Router (v1)
│   │   ├── schemas        # Pydantic-Modelle
│   │   ├── services       # Hintergrunddienste (Telemetry)
│   │   ├── utils          # Helfer (IDs, Datumsfunktionen)
│   │   ├── auth.py        # Authentifizierungs- und RBAC-Layer
│   │   ├── config.py      # Settings via pydantic-settings
│   │   ├── events.py      # Async EventBus
│   │   ├── lifecycle.py   # Startup/Shutdown Hooks
│   │   ├── main.py        # FastAPI Factory
│   │   ├── state.py       # AppState mit CRUD-Hilfen
│   │   └── storage.py     # Thread-sichere In-Memory Stores
│   └── app/tests          # Pytest-Smoketest für das Backend
├── docs
│   └── admin-automation-dashboard-pro.md  # Ausschreibungsdokument
├── frontend
│   ├── electron           # Electron Main/Preload-Skripte
│   ├── src
│   │   ├── components     # React-Komponenten (Header, Dashboard, Sidebar, Login)
│   │   ├── hooks          # WebSocket Hook
│   │   ├── services       # API-Client
│   │   ├── store          # Zustand Stores
│   │   ├── types          # Gemeinsame TS-Typen/Globals
│   │   ├── App.tsx        # App-Shell & Routing der Views
│   │   └── main.tsx       # Einstiegspunkt
│   ├── package.json       # npm-Konfiguration
│   └── vite.config.ts     # Vite-Konfiguration
├── requirements.txt       # Python-Abhängigkeiten
└── README.md
```

## Backend starten

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

* Standard-Port: `http://localhost:8000`
* WebSocket: `ws://localhost:8000/ws/events`
* Demo-Zugangsdaten:
  * `admin` / `admin123`
  * `operator` / `operator123`
  * `developer` / `dev123`
  * `viewer` / `viewer123`

## Frontend entwickeln

```bash
cd frontend
npm install
npm run dev
```

Der Befehl startet Vite (Port 5173) und Electron parallel. Über `BACKEND_URL` kann ein anderer Backend-Endpunkt gesetzt werden (z. B. `BACKEND_URL=http://localhost:8001 npm run dev`).

## Tests

* Backend: `pytest`
* Syntax-Check: `python -m compileall backend`
* Frontend: `npm run lint`

## Erweiterungsideen

* Persistente Datenbank (z. B. PostgreSQL) statt In-Memory-Stores.
* Asynchrones Worker-System für Routine-Ausführung (Celery, Dramatiq).
* Vollständige Umsetzung der Geräte-Kommunikation, API-Proxys oder HTTP-Server-Deployments.
* Deployment-Skripte (Docker Compose) für ein reproduzierbares Setup.

Das Projekt liefert eine vollständige Demo-Umgebung, um das im Pflichtenheft geforderte Produkt iterativ weiterzuentwickeln.
