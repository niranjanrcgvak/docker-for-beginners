# Docker for Beginners

Material for a hands-on Docker seminar, written for developers who already know Python, HTML/CSS/JavaScript, REST APIs, JSON, Git and SQL.

**Presented by:** Niranjan R

## What is inside

| Folder | Contents |
|---|---|
| `demo/` | The Team Notes demo app: a Flask REST API with an HTML/JavaScript front end, backed by PostgreSQL, run with Docker Compose |

## What you will learn

- Why Docker exists, and how containers differ from virtual machines
- Images, containers, Dockerfiles and registries
- Running, inspecting and removing containers
- Volumes, ports and networks
- Running a multi-container app with one command
- Best practices and where to go next

## Requirements

- Docker Desktop, or Docker Engine with the Compose plugin
- A terminal (PowerShell on Windows, any shell on macOS or Linux)
- A modern browser (Chrome or Edge recommended)

Check your organisation's licence terms before using Docker Desktop for work projects.

## Quick start: run the demo

```
git clone https://github.com/<your-username>/docker-for-beginners.git
cd docker-for-beginners/demo
docker compose up --build
```

Open <http://localhost:5000>, add a few notes, then try:

```
docker compose ps                  # what is running
docker compose logs -f web         # live logs of the app
docker compose down                # stop, keep the data (volume)
docker compose up -d               # start again, the notes are still there
docker compose down -v             # stop and delete the data
```

## The demo app

```
Browser  ->  web container (Flask REST API)  ->  db container (PostgreSQL + volume)
```

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/notes` | List all notes |
| POST | `/api/notes` | Add a note, body `{"text": "..."}` |
| DELETE | `/api/notes/<id>` | Delete a note |
| GET | `/health` | Health check |

Port 5000 is published to your laptop. PostgreSQL's port 5432 stays inside the Docker network. Notes are stored in the `notes_data` volume.

The demo README (`demo/README.md`) also shows how to run the same app without Compose, using `docker build`, `docker network create` and `docker run`.

## Using the slides

Open https://niranjanrcgvak.github.io/docker-for-beginners in a browser.

| Key | Action |
|---|---|
| Right arrow, Space | Next slide |
| Left arrow | Previous slide |
| Home, End | First or last slide |
| O | List of all slides |
| F | Full screen |

## Learning path after this seminar

1. Containerise one of your own projects
2. Multi-stage builds, `.env` files and secrets, healthchecks, pushing to a registry
3. CI/CD pipelines, image scanning, Compose profiles and Watch
4. Kubernetes, observability and supply-chain security

## Licence

The code and notes are released under the [MIT Licence](LICENSE).

The Docker name and logo are trademarks of Docker, Inc. The logo appears in the slides for identification only, and is not covered by the MIT Licence. See Docker's brand guidelines before redistributing the slides.
