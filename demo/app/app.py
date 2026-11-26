"""Tiny "Team Notes" REST API.

Flask + PostgreSQL. Everything configurable through environment variables
so the SAME image runs on any laptop (that is the Docker lesson!).
"""
import os
import time

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

DB_SETTINGS = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "notes"),
    "user": os.getenv("DB_USER", "notes_user"),
    "password": os.getenv("DB_PASSWORD", "notes_pass"),
}


def get_conn():
    return psycopg2.connect(**DB_SETTINGS)


def init_db(retries=10, delay=2):
    """Create the table. Retry because the DB container may still be booting."""
    for attempt in range(1, retries + 1):
        try:
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                        id SERIAL PRIMARY KEY,
                        text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                    """
                )
            print("Database ready", flush=True)
            return
        except psycopg2.OperationalError as exc:
            print(f"DB not ready (attempt {attempt}/{retries}): {exc}", flush=True)
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database")


@app.get("/")
def home():
    return send_from_directory("static", "index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/notes")
def list_notes():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT id, text, created_at FROM notes ORDER BY id DESC")
        rows = cur.fetchall()
    for row in rows:
        row["created_at"] = row["created_at"].isoformat(timespec="seconds")
    return jsonify(rows)


@app.post("/api/notes")
def add_note():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify(error="text is required"), 400
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id, text, created_at",
            (text,),
        )
        row = cur.fetchone()
    row["created_at"] = row["created_at"].isoformat(timespec="seconds")
    return jsonify(row), 201


@app.delete("/api/notes/<int:note_id>")
def delete_note(note_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
