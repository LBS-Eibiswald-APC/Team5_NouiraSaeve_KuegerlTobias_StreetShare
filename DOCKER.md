# Docker Setup

## Start everything

```bash
docker compose up --build
```

## Services

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- MySQL: `localhost:3306`

## Automatic bootstrap

Beim ersten Start der Datenbank wird `DB/StreetShare.sql` automatisch importiert.

Zusätzlich werden beim Start des Backends automatisch sichergestellt:

- die Rollen `Admin` und `User`
- ein Admin-Account aus den Compose-Umgebungsvariablen

Standardwerte:

- E-Mail: `admin@streetshare.at`
- Anzeigename: `admin`
- Passwort: `admin123`

## Stop

```bash
docker compose down
```

## Reset database volume

```bash
docker compose down -v
```

Danach wird die Datenbank beim nächsten `docker compose up --build` wieder frisch aus `DB/StreetShare.sql` aufgebaut.
