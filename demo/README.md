# Team Notes – Docker demo (Flask + PostgreSQL)

## Run it (Docker Desktop must be running)
    docker compose up --build        # first time
    open http://localhost:5000

## Useful commands during the demo
    docker compose ps                # what is running
    docker compose logs -f web       # live logs of the app
    docker compose exec db psql -U notes_user -d notes -c "SELECT * FROM notes;"
    docker compose down              # stop, KEEP data (volume)
    docker compose down -v           # stop and DELETE data

## Without Compose (the manual way, for teaching)
    docker build -t notes-web ./app
    docker network create notes-net
    docker run -d --name db --network notes-net -e POSTGRES_DB=notes -e POSTGRES_USER=notes_user -e POSTGRES_PASSWORD=notes_pass postgres:16-alpine
    docker run -d --name web --network notes-net -p 5000:5000 -e DB_HOST=db notes-web
    # cleanup
    docker rm -f web db && docker network rm notes-net

## API
GET /api/notes · POST /api/notes {"text": "..."} · DELETE /api/notes/<id> · GET /health
